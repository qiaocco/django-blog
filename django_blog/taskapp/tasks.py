import datetime
import subprocess

from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.core.mail import EmailMessage

from .celery import app as celery_app

logger = get_task_logger(__name__)


@celery_app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")  # pragma: no cover


@shared_task(bind=True)
def send_mail(self, subject, body, to, attachments=None):
    logger.info("发送邮件 starting...")
    email = EmailMessage(
        subject=subject, body=body, from_email=settings.EMAIL_HOST_USER, to=to
    )
    if attachments:
        for attachment in attachments:
            email.attach(*attachment)
    try:
        email.send(fail_silently=False)
    except Exception as exc:
        logger.exception(f"邮件发送失败:{exc}, to: {to}")
        raise self.retry(exc=exc, countdown=5 * 60, max_retries=3)  # 每5分钟重试一次，共3次
    else:
        logger.info(f"邮件发送成功: {to}")


@celery_app.task
def mysql_backup():
    BACKUP_DIR_NAME = "/tmp"
    FILE_PREFIX = "db_backup_"
    FILE_SUFFIX_DATE_FORMAT = "%Y%m%d"
    PYTHON_PATH = "/home/jason/.venv/blog_py3.6_env/bin/python"

    timestamp = datetime.date.today().strftime(FILE_SUFFIX_DATE_FORMAT)
    backup_filename = BACKUP_DIR_NAME + "/" + FILE_PREFIX + timestamp + ".sql"

    backup_command = (
        f"{PYTHON_PATH} manage.py dumpdata --exclude auth.permission --exclude contenttypes "
        f"-o {backup_filename}"
    )
    subprocess.call(backup_command.split())
    send_mail.delay(
        subject=f"数据库备份-{timestamp}",
        body="备份好啦！",
        to=[settings.EMAIL_HOST_USER],
        attachments=[
            (backup_filename, open(backup_filename, "r").read(), "text/plain")
        ],
    )
