from push.serializers import TokenSendRequestSerializer
from push.repositories import PushRepository
from push.models import Token
from firebase_admin import messaging
from datetime import datetime
from django.shortcuts import get_list_or_404
from menu.models import Menu
import logging

class PushService:
    def __init__(self, push_repo: PushRepository):
        self._push_repo = push_repo

    def send_push_token(self, request_data: dict):
        token_send_request_serializer = TokenSendRequestSerializer(data=request_data)
        token_send_request_serializer.is_valid(raise_exception=True)
        token_data = token_send_request_serializer.validated_data

        new_token = Token(push_token=token_data.get('push_token'))
        self._push_repo.save_token(new_token)

    def send_push_alarm(self, timezone: str):
        tokens: list[Token] = self._push_repo.find_all_valid_tokens()
        token_ids: list[str] = [token.push_token for token in tokens]
        
        menu_string_set, title = self._get_menu_data_set_and_message_title(timezone)
        try:
            message = messaging.MulticastMessage(
                notification = messaging.Notification(
                title=f'🍽️ 돔토리 {title}식단 알리미',
                body=menu_string_set
            ),
                tokens=token_ids,
            )
            messaging.send_multicast(message)
        except Exception as e:
            logging.ERROR("PUSH 에러 발생:", e)

    def make_token_invalid(self, request_data):
        token_send_request_serializer = TokenSendRequestSerializer(data=request_data)
        token_send_request_serializer.is_valid(raise_exception=True)
        token_data = token_send_request_serializer.validated_data

        token: Token = self._push_repo.find_token_by_token(token_data.get('push_token'))
        token.is_valid = False
        self._push_repo.save_token(token)

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