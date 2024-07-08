from push.domains import PushRepository
from board.repositories import BoardRepository
from firebase_admin import messaging
from datetime import datetime
from django.shortcuts import get_list_or_404
from menu.models import Menu
from utils.connect_dynamodb import get_dynamodb_table
from boto3.dynamodb.conditions import Key
from push.serializers import PushListResponseSerializer, PushCheckRequestSerialzier
from board.models import Post
from member.domains import MemberRepository
from message.domains import MessageRoom, Message

class PushService:
    def __init__(self, push_repository: PushRepository, board_repository: BoardRepository, member_repository: MemberRepository):
        self._push_repository = push_repository
        self._board_repository = board_repository
        self._member_repository = member_repository
        self._table = get_dynamodb_table('domtory')
    
    def make_menu_push_notification_data(self, event, timezone: str):
        valid_devices = self._push_repository.find_all_devices_with_member_and_notification_detail()
        member_ids = {valid_device.member_id for valid_device in valid_devices if getattr(valid_device.member.notificationdetail, timezone)}
        valid_device_tokens = [valid_device.device_token for valid_device in valid_devices if getattr(valid_device.member.notificationdetail, timezone)]
        menu_string_set, timezone = self._get_menu_data_set_and_message_title(timezone)
        title = f"🐿️ 오늘의 돔토리 {timezone} 메뉴에요. 🍽️"
        return self._wrapping_notification_data(member_ids, title, menu_string_set, valid_device_tokens)
    
    def make_comment_push_notification_data(
            self,
            event: str,
            comment_id: int
        ):
        # 코멘트를 post와 parent를 조인해서 가져온다.
        comment = self._board_repository.find_comment_by_comment_id_with_post_and_parent(comment_id)
        if not comment.parent: # 댓글일 때. 이 if, else 문에서 device_tokens과 member_ids를 만든다.
            device_tokens, devices = self._get_device_tokens_and_devices_when_comment(comment)

            # 가져온 devices들로 member_id를 뽑아낸다. 본인의 글에 댓글을 달 경우 devices는 None으로 오게 된다.
            if devices:
                member_ids = {device.member_id for device in devices}
            else:
                member_ids = None

            title = f'🐿️ \'{comment.post.title}\'글에 새로운 댓글이 달렸어요.'
        else: # 대댓글일 때
            device_tokens, member_ids = self._get_device_tokens_and_member_ids_when_reply(comment)
            title = f'🐿️ \'{comment.post.title}\'글에 새로운 대댓글이 달렸어요.'
        
        # 댓글 대댓글의 푸시 알림은 이동을 위한 postId와 boardId가 필요하다.
        data={
            'postId': str(comment.post_id),
            'boardId': str(comment.post.board_id)
        }
        return self._wrapping_notification_data(member_ids, title, comment.body, device_tokens, data)

    def make_post_push_notification_data(self, event: str, post_id: int):
        notification_setting_map = {
            4: 'lightning_post',
            5: 'lost_item'
        }
        post: Post = self._board_repository.find_post_by_id(post_id)
        notification_setting = notification_setting_map.get(post.board_id)
        if notification_setting:
            valid_devices = self._push_repository.find_all_devices_with_member_and_notification_detail()
            member_ids = {
                valid_device.member_id for valid_device in valid_devices if getattr(valid_device.member.notificationdetail, notification_setting)
            }
            valid_device_tokens = [
                valid_device.device_token for valid_device in valid_devices if getattr(valid_device.member.notificationdetail, notification_setting)
            ]
        else:
            valid_devices = self._push_repository.find_all_devices()
            valid_device_tokens = [valid_device.device_token for valid_device in valid_devices]
            member_ids = {valid_device.member_id for valid_device in valid_devices}

        title_dict = {
            4 : f'🐿️ ⚡️새로운 번개모임⚡️이 생겼어요!',
            5 : f'🐿️ 분실물 게시판에 글이 올라왔어요!',
            6 : f'🐿️ 새로운 자율회 공지사항이에요! 📢'
        }
        title = title_dict.get(post.board_id)
        data={
            'postId': str(post.id),
            'boardId': str(post.board_id)
        }
        return self._wrapping_notification_data(member_ids, title, post.title, valid_device_tokens, data)

    def make_admin_push_notification_data(self, event: str, title: str, body: str):
        valid_devices = self._push_repository.find_all_devices()
        member_ids = {valid_device.member_id for valid_device in valid_devices}
        valid_device_tokens = [valid_device.device_token for valid_device in valid_devices]
        return self._wrapping_notification_data(member_ids, title, body, valid_device_tokens)
    
    def make_message_push_notification_data(self, event: str, message: Message):
        message_room = MessageRoom.objects.get(id=message.message_room_id)
        if message_room:
            title = f"🐿️ {message_room.board}에서 쪽지가 도착했어요!"
            body = message.body[:10] + "..."
        valid_devices = self._push_repository.find_devices_by_member_id(message.sender_id)
        valid_device_tokens = [valid_device.device_token for valid_device in valid_devices]
        data = {
            "messageRoomId": str(message.id)
        }
        return self._wrapping_notification_data([message.sender_id], title, body, valid_device_tokens, data)
    
    def make_multicast_message(self, notification_data: dict):
        multicast_extra_data = {
            "tokens": notification_data.get('tokens')
        }
        # 만약에 data 있다면 message에 포함시킨다.
        if notification_data.get('data'):
            multicast_extra_data['data'] = notification_data.get('data')

        # 알림 필수 정보를 삽입한다.
        message = messaging.MulticastMessage(
            notification = messaging.Notification(
            title=notification_data.get('title'),
            body=notification_data.get('body')
        ),
        **multicast_extra_data # 그 외 multicast 부가 정보를 언패킹한다.
        )
        return message

    def save_push_notifications(self, notification_data: dict):
        # member_ids가 존재하지 않으면, 저장할 필요가 없다. 본인 글에 본인이 댓글, 대댓글을 단 경우이다.
        member_ids: set | None = notification_data.get('member_ids')
        if not member_ids:
            return notification_data
        pushed_at = str(datetime.now())
        item = {
            'pushedAt': pushed_at,
            'title': notification_data.get('title'),
            'body': notification_data.get('body'),
            'isChecked': 0
        }
        # 만약 데이터가 있다면 data에 있는 정보들을 item에 추가시킨다.
        if notification_data.get('data'):
            data: dict = notification_data.get('data')
            for key, value in data.items():
                item[key] = value
            # notification_data의 data에 pushedAt을 추가한다.
            notification_data.get('data')['pushedAt'] = pushed_at

        # batch_writer를 활용해 한번에 저장시킨다. 이 때 멤버 아이디도 추가한다.
        with self._table.batch_writer() as batch:
            for member_id in member_ids:
                new_item = item.copy()
                new_item['memberId'] = member_id
                batch.put_item(Item=new_item)

        return notification_data
    
    def send_push_notification(self, message):
        response = messaging.send_multicast(message)
        return response

    def get_push_list(self, request_user):
        query_params = {
            'KeyConditionExpression': Key('memberId').eq(request_user.id),
            'ScanIndexForward': False,
            'Limit': 20
        }
        response = self._table.query(**query_params).get('Items')
        for item in response:
            pushed_at = datetime.strptime(item['pushedAt'], '%Y-%m-%d %H:%M:%S.%f')
            item['transformedPushedAt'] = pushed_at.strftime('%m/%d %H:%M')

        return PushListResponseSerializer(response, many=True).data
    
    def check_push_notification(self, request_data):
        push_check_request_serializer = PushCheckRequestSerialzier(data=request_data)
        push_check_request_serializer.is_valid(raise_exception=True)
        push_data = push_check_request_serializer.validated_data
        
        self._table.update_item(
            Key={"memberId": push_data.get('member_id'), "pushedAt": push_data.get('pushed_at')},
            UpdateExpression="set isChecked=:c",
            ExpressionAttributeValues={":c": True},
            ReturnValues="UPDATED_NEW",
        )

    def delete_push_notification(self, request_data):
        push_check_request_serializer = PushCheckRequestSerialzier(data=request_data)
        push_check_request_serializer.is_valid(raise_exception=True)
        push_data = push_check_request_serializer.validated_data
        self._table.delete_item(
            Key={"memberId": push_data.get('member_id'), "pushedAt": push_data.get('pushed_at')},
        )

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
        target_table_name = timezone
        menu: list[Menu] = get_list_or_404(Menu.objects.prefetch_related(target_table_name), date_code=date_code)
        menu_set = getattr(menu[0], target_table_name).all()

        menu_string_set: str = ''
        for menu in menu_set:
            menu_string_set += f"{menu.name}, "

        last_comma = menu_string_set.rfind(',')
        if last_comma != -1:
            menu_string_set = menu_string_set[:last_comma] + menu_string_set[last_comma+1:]
    
        kor_timezone = title_mapping.get(timezone)
        return menu_string_set, kor_timezone
    
    def _get_device_tokens_and_devices_when_comment(self, comment):
        member_id = comment.post.member_id
        member = self._member_repository.find_member_with_notification_detail_by_id(member_id)

        # 코멘트 알림이 되어있지 않은 멤버에게는 알림이 가지 않게
        if not member.notificationdetail.comment:
            return [], None
        devices = self._push_repository.find_devices_by_member_id(member_id)
        if comment.member_id == comment.post.member_id:
            return [], None
        return list(set(device.device_token for device in devices)), set(devices)
    
    def _get_device_tokens_and_member_ids_when_reply(self, comment):
        same_parent_comments = self._board_repository.find_comments_by_parent_with_member_and_notification_detail(comment.parent)
        member_ids = [
            same_parent_comment.member_id
            for same_parent_comment in same_parent_comments
            if same_parent_comment.member.notificationdetail.reply and same_parent_comment.member_id != comment.member_id # 부모가 같은 대댓글 중 본인에게는 알림이 가지 않게
        ]
        member_ids += [
            member.id
            for member in (comment.post.member, comment.parent.member)
            if member.notificationdetail.reply and member.id != comment.member_id
        ] # 본인의 댓글에 대댓글을 달거나 본인의 글에 있는 댓글에 대댓글을 달 때를 알림이 가지 않게
        devices = self._push_repository.find_devices_by_member_ids(member_ids)
        return list(set(device.device_token for device in devices)), set(member_ids)
    
    def _wrapping_notification_data(self, member_ids: list[int], title: str, body: str, tokens: list[str], data=None):
        notification_data = {
            "member_ids": member_ids,
            "title": title,
            "body": body,
            "tokens": tokens
        }
        if data:
            notification_data['data'] = data
        return notification_data