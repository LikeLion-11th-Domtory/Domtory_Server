from push.domains import NotificationDetail
from django.shortcuts import get_object_or_404

class NotificationDetailRepository:

    def find_notification_detail_by_member_id(self, member_id: int):
        return get_object_or_404(NotificationDetail, member_id=member_id)
    
    def save_notification_detail(self, notification_detail: NotificationDetail):
        notification_detail.save()