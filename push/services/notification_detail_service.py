from push.domains import NotificationDetail, NotificationDetailRepository
from push.serializers import NotificationDetailSerializer

class NotificationDetailService:
    def __init__(self, notification_detail_repository: NotificationDetailRepository):
        self._notification_detail_repository = notification_detail_repository
    
    def get_notification_detail(self, user_data):
        notification_detail: NotificationDetail = self._notification_detail_repository.find_notification_detail_by_member_id(user_data.id)
        serialzier = NotificationDetailSerializer(notification_detail)
        return serialzier.data
    
    def change_notification_detail(self, request_data, user_data):
        notification_detail: NotificationDetail = self._notification_detail_repository.find_notification_detail_by_member_id(user_data.id)

        notification_detail_serializer = NotificationDetailSerializer(data=request_data)
        notification_detail_serializer.is_valid(raise_exception=True)
        notification_detail_data = notification_detail_serializer.validated_data
        self._save_notification_detail_object(notification_detail, notification_detail_data)

    def _save_notification_detail_object(self, notification_detail: NotificationDetail, notification_detail_data: dict):
        notification_detail.breakfast = notification_detail_data.get('breakfast')
        notification_detail.lunch = notification_detail_data.get('lunch')
        notification_detail.dinner = notification_detail_data.get('dinner')
        notification_detail.lightning_post = notification_detail_data.get('lightning_post')
        notification_detail.comment = notification_detail_data.get('comment')
        notification_detail.reply = notification_detail_data.get('reply')
        notification_detail.lost_item = notification_detail_data.get('lost_item')
        notification_detail.message = notification_detail_data.get('message')
        self._notification_detail_repository.save_notification_detail(notification_detail)
