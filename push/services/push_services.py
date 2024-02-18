from push.serializers import TokenRequestSerializer
from push.domains import PushRepository
from board.repositories import BoardRepository
from firebase_admin import messaging
from datetime import datetime
from django.shortcuts import get_list_or_404
from menu.models import Menu
from push.domains.device import Device

class PushService:
    def __init__(self, push_repository: PushRepository, board_repository: BoardRepository):
        self._push_repository = push_repository
        self._board_repository = board_repository

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
        valid_devices = self._push_repository.find_all_devices()
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
    
    def delete_device(self, request_data, request_user):
        token_send_request_serializer = TokenRequestSerializer(data=request_data)
        token_send_request_serializer.is_valid(raise_exception=True)
        token_data = token_send_request_serializer.validated_data

        device: Device = self._push_repository.find_device_by_token_and_member(token_data.get('push_token'), request_user)

        self._push_repository.delete_device(device)

    def send_push_notification(self, message):
        response = messaging.send_multicast(message)
        return response

    def make_comment_push_notification_message(
            self,
            event: str,
            comment_id: int
        ):
        comment = self._board_repository.find_comment_by_comment_id_with_post_and_parent(comment_id)
        if not comment.parent: # 댓글일 때
            device_tokens = self._find_device_tokens_when_comment(comment)
            title = f'🐿️ \'{comment.post.title}\'글에 새로운 댓글이 달렸어요.'
        else: # 대댓글일 때
            device_tokens = self._find_device_tokens_when_reply(comment)
            title = f'🐿️ \'{comment.post.title}\'글에 새로운 대댓글이 달렸어요.'

        message = messaging.MulticastMessage(
            notification = messaging.Notification(
            title=title,
            body=comment.body
        ),
        data={
            'postId': str(comment.post_id),
            'boardId': str(comment.post.board_id)
        },
        tokens=device_tokens,
        )
        return message

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
    
    def _find_device_tokens_when_comment(self, comment):
        member_id = comment.post.member_id
        devices = self._push_repository.find_devices_by_member_id(member_id)
        if comment.member_id == comment.post.member_id:
            return []
        return list(set(device.device_token for device in devices))
    
    def _find_device_tokens_when_reply(self, comment):
        same_parent_comments = self._board_repository.find_comments_by_parent_with_member(comment.parent)
        member_ids = [
            same_parent_comment.member_id
            for same_parent_comment in same_parent_comments
            if same_parent_comment.member_id != comment.member_id # 부모가 같은 대댓글 중 본인에게는 알림이 가지 않게
        ]
        member_ids += [
            member_id
            for member_id in (comment.post.member_id, comment.parent.member_id)
            if member_id != comment.member_id
        ] # 본인의 댓글에 대댓글을 달거나 본인의 글에 있는 댓글에 대댓글을 달 때를 알림이 가지 않게
        devices = self._push_repository.find_devices_by_member_ids(member_ids)
        return list(set(device.device_token for device in devices))