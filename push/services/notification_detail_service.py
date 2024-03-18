from push.domains import NotificationDetail, NotificationDetailRepository
from push.serializers import NotificationDetailResponseSerializer

class NotificationDetailService:
    def __init__(self, notification_detail_repository: NotificationDetailRepository):
        self._notification_detail_repository = notification_detail_repository
    
    def get_notification_detail(self, user_data):
        notification_detail: NotificationDetail = self._notification_detail_repository.find_notification_detail_by_member_id(user_data.id)
        serialzier = NotificationDetailResponseSerializer(notification_detail)
        return serialzier.data