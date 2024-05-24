from rest_framework import permissions

from message.domains.message_models import MessageRoom


class IsParticipant(permissions.BasePermission):
    def has_permission(self, request, view):
        message_room_id = view.kwargs.get('message_room_id')
        if not message_room_id:
            return False
        try:
            message_room = MessageRoom.objects.get(id=message_room_id)
        except MessageRoom.DoesNotExist:
            return False

        if request.user == message_room.first_sender or request.user == message_room.first_receiver:
            return True
        return False