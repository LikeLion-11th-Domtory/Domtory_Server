from django.contrib import admin
from .domains import AdminPushNotification, Device
from push.tasks import send_push_notification_handler
from datetime import datetime
import pytz

class AdminPushNotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'staff_member', 'title', 'body', 'created_at', 'notification_type']
    readonly_fields = ['staff_member', 'created_at']
    
    def save_model(self, request, obj, form, change):
        notification_type = form.cleaned_data['notification_type']
        push_title = form.cleaned_data['title']
        push_body = form.cleaned_data['body']
        title, body = self._make_push_title_and_body(notification_type, push_title, push_body)
        obj.created_at = datetime.now(pytz.timezone('Asia/Seoul'))
        if not change:
            obj.staff_member = request.user
        if push_body:
            if push_title == '' and notification_type in ('normal'):
                return
            send_push_notification_handler.delay('admin-notification-event', None, title=title, body=body)
        super().save_model(request, obj, form, change)
    
    def _make_push_title_and_body(self, notification_type: str, push_title: str, push_body: str):
        if notification_type == 'normal':
            return "🐿️ " + push_title, push_body
        elif notification_type == 'update':
            return "🐿️ 돔토리 업데이트 알림", f"{push_body} 버전이 새로 출시됐어요! 업데이트 해주실거죠? 🥹"
        elif notification_type == 'emergency':
            return "📢🐿️ 돔토리 긴급 공지 🚨", push_body

admin.site.register(AdminPushNotification, AdminPushNotificationAdmin)
admin.site.register(Device)