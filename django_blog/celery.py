import logging
import os

from celery import Celery, shared_task
from django.apps import AppConfig, apps
from django.conf import settings
from django.core.mail import EmailMessage

if not settings.configured:
    # set the default Django settings module for the 'celery' program.
    profile = os.environ.get('DJANGO_BLOG_PROFILE', 'develop')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.{}".format(profile))

app = Celery('django_blog')


class CeleryConfig(AppConfig):
    name = 'django_blog.taskapp'
    verbose_name = 'Celery Config'

    def ready(self):
        # Using a string here means the worker will not have to
        # pickle the object when using Windows.
        # - namespace='CELERY' means all celery-related configuration keys
        #   should have a `CELERY_` prefix.
        # import pdb;pdb.set_trace()
        app.config_from_object('django.conf:settings', namespace='CELERY')

        installed_apps = [app_config.name for app_config in apps.get_app_configs()]
        app.autodiscover_tasks(lambda: installed_apps, force=True)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))  # pragma: no cover


logger = logging.getLogger(__name__)


@shared_task
def send_mail(subject, body, to, attachments=None):
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.EMAIL_HOST_USER,
        to=to
    )
    if attachments:
        for attachment in attachments:
            email.attach_file(attachment)
    try:
        email.send(fail_silently=False)
    except Exception as e:
        logging.exception('邮件发送失败. to: {}'.format(to))
    else:
        logger.info('发送:《{subject}》到{to}'.format(subject=subject, to=to))


@app.task
def test(arg):
    print(arg)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test_beat every 10 seconds
    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10 seconds')
