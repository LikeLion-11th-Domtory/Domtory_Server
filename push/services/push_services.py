from push.serializers import TokenRequestSerializer
from push.domains import PushRepository
from firebase_admin import messaging
from datetime import datetime
from django.shortcuts import get_list_or_404
from menu.models import Menu
from push.domains.device import Device

class PushService:
    def __init__(self, push_repository: PushRepository):
        self._push_repository = push_repository

    def send_push_token(self, request_data: dict, request_user: Menu):
        token_send_request_serializer = TokenRequestSerializer(data=request_data)
        token_send_request_serializer.is_valid(raise_exception=True)
        token_data = token_send_request_serializer.validated_data

        device = Device(
            device_token=token_data.get('push_token'),
            member=request_user,
        )
        self._push_repository.save_device(device)
    
    def make_menu_push_notification_message(self, event, timezone: str):
        valid_devices = self._push_repository.find_all_valid_device()
        valid_device_tokens = [valid_device.device_token for valid_device in valid_devices]
        menu_string_set, title = self._get_menu_data_set_and_message_title(timezone)

        message = messaging.MulticastMessage(
            notification = messaging.Notification(
            title=f'🐿️ 돔토리 {title}식단 알리미',
            body=menu_string_set
        ),
            tokens=valid_device_tokens,
        )
        return message
    
    def make_token_invalid(self, request_data):
        token_send_request_serializer = TokenRequestSerializer(data=request_data)
        token_send_request_serializer.is_valid(raise_exception=True)
        token_data = token_send_request_serializer.validated_data

        device: Device = self._push_repository.find_device_by_token(token_data.get('push_token'))
        device.set_valid(False)
        self._push_repository.save_device(device)

    def send_push_notification(self, message):
        response = messaging.send_multicast(message)
        return response

    def make_comment_push_notification_message(
            self,
            event: str,
            comment_id: int
        ):
        # from django.db.models import Q
        # comment = get_object_or_404(Comment.objects.select_related('post__member', 'parent__member'), id=comment_id)
        # if not comment.parent_id: # 만약 코멘트가 댓글이면
        #     member = comment.post.member
        #     devices = Device.objects.filter(member_id=member.id)
        #     device_tokens = [device.device.token for device in devices]
        #     title = '🐿️ 새로운 댓글이 달렸어요.'

        # else: # 만약 코멘트가 대댓글이면
        #     comments = Comment.objects.filter(parent_id=comment.parent_id).select_related('member')
        #     member_ids = [comment.member.id for comment in comments]
        #     devices = Device.objects.filter(Q(member_id=comment.post.member.id) | Q(member_id=comment.parent.member.id) | Q(member_id__in=member_ids))
        #     device_tokens = [device.device_token for device in devices]
        #     title = '🐿️ 새로운 대댓글이 달렸어요.'

        # message = messaging.MulticastMessage(
        #     notification = messaging.Notification(
        #     title=f'🐿️ 돔토리 {title}식단 알리미',
        #     body=comment.body
        # ),
        #     tokens=device_tokens,
        # )
        # return message
        pass

    def _make_today_date_code(self):
        now = datetime.now()
        formatted_now = now.strftime('%y%m%d')
        return formatted_now
    
    def _get_menu_data_set_and_message_title(self, timezone: str):
        title_mapping: dict = {
            "breakfast": "아침",
            "lunch": "점심",
            "dinner": "저녁"
        }
        date_code: str = self._make_today_date_code()
        target_table_name = timezone + 's'
        menu: list[Menu] = get_list_or_404(Menu.objects.prefetch_related(target_table_name), date_code=date_code)
        menu_set = getattr(menu[0], target_table_name).all()

        menu_string_set: str = ''
        for menu in menu_set:
            menu_string_set += f"{menu.name}, "

        last_comma = menu_string_set.rfind(',')
        if last_comma != -1:
            menu_string_set = menu_string_set[:last_comma] + menu_string_set[last_comma+1:]
    
        title = title_mapping.get(timezone)
        return menu_string_set, title