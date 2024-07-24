
from server.celery import app

from report.tasks import *


def async_unban_member_status(report_id, ban_period):
    print("member_id = ", report_id, "& ban_period = ", ban_period)

    # countdown = int(ban_period) * 60 * 60 * 24 #ban_period(3, 7, 30일)을 초로 변환
    countdown = int(ban_period) * 60
    unban_member_task.apply_async((report_id,), countdown=countdown)
    return