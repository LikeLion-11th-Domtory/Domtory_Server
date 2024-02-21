from push.serializers import TokenRequestSerializer
from push.domains import PushRepository
from board.repositories import BoardRepository
from menu.models import Menu
from push.domains.device import Device

class DeviceService:
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
    
    def delete_device(self, request_data, request_user):
        token_send_request_serializer = TokenRequestSerializer(data=request_data)
        token_send_request_serializer.is_valid(raise_exception=True)
        token_data = token_send_request_serializer.validated_data

        device: Device = self._push_repository.find_device_by_token_and_member(token_data.get('push_token'), request_user)

        self._push_repository.delete_device(device)