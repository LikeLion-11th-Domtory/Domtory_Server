from celery import Task
from server.celery import app
from push.containers import PushContainer
import logging

class RetryTask(Task):
    acks_late = True
    max_retries = 3

@app.task(bind=True, base=RetryTask)
def send_push_notification_handler(
        self,
        event: str,
        timezone: str=None,
        comment_id: int=None
    ):
    try:
        push_service = PushContainer.push_service()
        message = None
        if event == 'menu-scheule-event':
            message = push_service.make_menu_push_notification_message(event, timezone)
        elif event == 'comment-notification-event':
            message = push_service.make_comment_push_notification_message(event, comment_id)
        response = push_service.send_push_notification(message)

        for idx, resp in enumerate(response.responses):
            if resp.success:
                logging.info(f'Successfully sent message: {resp.message_id}')
            else:
                logging.error(f'FCM 전송 에러: {resp.exception}')
                self.retry(countdown=5**self.request.retries)

    except Exception as e:
        logging.error(f'send_menu_push_notification_beat 에러: {e}')
        self.retry(countdown=5**self.request.retries)