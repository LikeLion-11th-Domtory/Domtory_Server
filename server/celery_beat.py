from server.celery import app
from celery.schedules import crontab
from datetime import timedelta 
#celery -A server celery_beat beat --loglevel info

app.conf.beat_schedule = {
    'schedule-breakfast-menu-notification': {
        'task': 'push.tasks.send_push_notification_task',
        'schedule': crontab(minute=0, hour=6),
        'args': ('menu-scheule-event', 'breakfast',)
    },
    'schedule-lunch-menu-notification': {
        'task': 'push.tasks.send_push_notification_task',
        'schedule': crontab(minute=30, hour=11),
        'args': ('menu-scheule-event', 'lunch',)
    },
    'schedule-dinner-menu-notification': {
        'task': 'push.tasks.send_push_notification_task',
        'schedule': crontab(minute=30, hour=17),
        'args': ('menu-scheule-event', 'dinner',)
    }
}