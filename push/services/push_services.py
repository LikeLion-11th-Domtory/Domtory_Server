from push.serializers import TokenSendRequestSerializer
from push.repositories import PushRepository
from push.models import Token

class PushService:
    def __init__(self, push_repo: PushRepository):
        self._push_repo = push_repo

    def send_push_token(self, request_data: dict):
        token_send_request_serializer = TokenSendRequestSerializer(data=request_data)
        token_send_request_serializer.is_valid(raise_exception=True)
        token_data = token_send_request_serializer.validated_data

        new_token = Token(push_token=token_data.get('push_token'))
        self._push_repo.save_token(new_token)