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
    print("Request: {0!r}".format(self.request))  # pragma: no cover


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
    MYSQL_CONTAINER_NAME = "django-blog_mysql_1"

    timestamp = datetime.date.today().strftime(FILE_SUFFIX_DATE_FORMAT)
    backup_filename = BACKUP_DIR_NAME + "/" + FILE_PREFIX + timestamp + ".sql"
    backup_file = open(backup_filename, "w")

    backup_command = f"docker exec -it {MYSQL_CONTAINER_NAME} /usr/bin/mysqldump -uroot -p123 django_blog"
    subprocess.call(backup_command.split(), stdout=backup_file)
    backup_file.close()
    send_mail.delay(
        subject=f"数据库备份-{datetime.date.today()}",
        body="备份好啦！",
        to=[settings.EMAIL_HOST_USER],
        attachments=[
            (backup_filename, open(backup_filename, "r").read(), "text/plain")
        ],
    )