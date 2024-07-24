
import logging
from celery import shared_task
from server.celery import app

from report.models.report_models import Report
from member.domains.member import Member

# @app.task(bind=True)
@shared_task(bind=True)
def unban_member_task(self, report_id):
    try:
        report = Report.objects.get(pk=report_id)
        if report.member_status != Report.MEMBER_BLOCK_CHOICES[0][0]:
            report.member_status = Report.MEMBER_BLOCK_CHOICES[0][0]

            if report.post:
                report.post.member.status = Member.MEMBER_STATUS_CHOICES[0][0]
                report.post.member.save()

                logging.info(f"Successfully unbanned member id {report.post.member.id}")

            elif report.comment:
                report.comment.member.status = Member.MEMBER_STATUS_CHOICES[0][0]
                report.comment.member.save()

                logging.info(f"Successfully unbanned member id {report.comment.member.id}")

            report.save()

    except Exception as e:
        logging.error(f"unban member status error: {e}")