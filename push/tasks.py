from celery import Task
from server.celery import app
from push.containers import PushContainer
import logging
from utils.exceptions import FCMSendException

class RetryTask(Task):
    acks_late = True
    max_retries = 3

@app.task(bind=True, base=RetryTask)
def send_push_notification_handler(
        self,
        event: str,
        timezone: str=None,
        comment_id: int=None,
        post_id: int=None,
        title: str=None,
        body: str=None
    ):
    try:
        push_service = PushContainer.push_service()
        notification_data = None
        
        # 받은 이벤트를 기반으로 분기해서 notification data를 만든다.  
        if event == 'menu-scheule-event': # 메뉴 알림일 때
            notification_data = push_service.make_menu_push_notification_data(event, timezone)
        elif event == 'comment-notification-event': # 댓글 알림일 때
            notification_data = push_service.make_comment_push_notification_data(event, comment_id)
        elif event == 'post-notification-event':
            notification_data = push_service.make_post_push_notification_data(event, post_id)
        elif event == 'admin-notification-event':
            notification_data = push_service.make_admin_push_notification_data(event, title, body)

        # 식단 알림은 저장하지 않는다.
        if event != 'menu-scheule-event':
            notification_data = push_service.save_push_notifications(notification_data)

        # notification data를 기반으로 multicast_message를 만든다.
        message = push_service.make_multicast_message(notification_data)
        response = push_service.send_push_notification(message)

        for idx, resp in enumerate(response.responses):
            if resp.success:
                logging.info(f'Successfully sent {event} message: {resp.message_id}')
            else:
                raise FCMSendException
    except Exception as e:
        if notification_data:
            error_title = notification_data.get('title', None)
            error_body = notification_data.get('body', None)
            logging.error(f'[{event}] message sent error: {e}\n title: {error_title}\n body: {error_body}')
        else:
            logging.error(f'[{event}] message sent error: {e}')