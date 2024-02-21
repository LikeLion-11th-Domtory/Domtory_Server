from push.domains import PushRepository
from board.repositories import BoardRepository
from firebase_admin import messaging
from datetime import datetime
from django.shortcuts import get_list_or_404
from menu.models import Menu
from utils.connect_dynamodb import get_dynamodb_table
from boto3.dynamodb.conditions import Key
from push.serializers import PushListResponseSerializer, PushCheckRequestSerialzier

class PushService:
    def __init__(self, push_repository: PushRepository, board_repository: BoardRepository):
        self._push_repository = push_repository
        self._board_repository = board_repository
        self._table = get_dynamodb_table('domtory')
    
    def make_menu_push_notification_data(self, event, timezone: str):
        valid_devices = self._push_repository.find_all_devices()
        member_ids = {valid_device.member_id for valid_device in valid_devices}
        valid_device_tokens = [valid_device.device_token for valid_device in valid_devices]
        menu_string_set, title = self._get_menu_data_set_and_message_title(timezone)
        notification_data = {
            'member_ids': member_ids,
            "title": f"🐿️ 오늘의 돔토리 {title} 메뉴에요. 🍽️",
            "body": menu_string_set,
            "tokens": valid_device_tokens
        }
        return notification_data 

    def send_push_notification(self, message):
        response = messaging.send_multicast(message)
        return response

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
        notification_data = {
            "member_ids": member_ids,
            "title": title,
            "body": comment.body,
            "tokens": device_tokens,
            "data": data
        }
        return notification_data
    
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
        now = datetime.now()

        # member_ids가 존재하지 않으면, 저장할 필요가 없다. 본인 글에 본인이 댓글, 대댓글을 단 경우이다.
        member_ids: set | None = notification_data.get('member_ids')
        if not member_ids:
            return
        
        item = {
            'pushedAt': str(now),
            'title': notification_data.get('title'),
            'body': notification_data.get('body'),
            'isChecked': 0
        }
        # 만약 데이터가 있다면 data에 있는 정보들을 item에 추가시킨다.
        if notification_data.get('data'):
            data: dict = notification_data.get('data')
            for key, value in data.items():
                item[key] = value

        #batch_writer를 활용해 한번에 저장시킨다. 이 때 멤버 아이디도 추가한다.
        with self._table.batch_writer() as batch:
            for member_id in member_ids:
                new_item = item.copy()
                new_item['memberId'] = member_id
                batch.put_item(Item=new_item)

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
    
        title = title_mapping.get(timezone)
        return menu_string_set, title
    
    def _get_device_tokens_and_devices_when_comment(self, comment):
        member_id = comment.post.member_id
        devices = self._push_repository.find_devices_by_member_id(member_id)
        if comment.member_id == comment.post.member_id:
            return [], None
        return list(set(device.device_token for device in devices)), set(devices)
    
    def _get_device_tokens_and_member_ids_when_reply(self, comment):
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
        return list(set(device.device_token for device in devices)), set(member_ids)