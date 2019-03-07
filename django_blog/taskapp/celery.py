import os

from celery import Celery
from celery.schedules import crontab
from django.apps import AppConfig, apps
from django.conf import settings

if not settings.configured:
    # set the default Django settings module for the 'celery' program.
    profile = os.environ.get("DJANGO_BLOG_PROFILE", "develop")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.{}".format(profile))


class MyCelery(Celery):
    def gen_task_name(self, name, module):
        if module.endswith('.tasks'):
            module = module[:-6]
        return super(MyCelery, self).gen_task_name(name, module)


app = MyCelery("django_blog")
# Using a string here means the worker will not have to
# pickle the object when using Windows.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")


class CeleryAppConfig(AppConfig):
    name = "django_blog.taskapp"
    verbose_name = "Celery Config"

    def ready(self):
        installed_apps = [app_config.name for app_config in apps.get_app_configs()]
        app.autodiscover_tasks(lambda: installed_apps, force=True)

        if os.environ.get("DJANGO_BLOG_PROFILE") == "production":
            import sentry_sdk
            from sentry_sdk.integrations.celery import CeleryIntegration

            sentry_sdk.init(dsn=settings.SENTRY_DSN, integrations=[CeleryIntegration()])


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    from .tasks import mysql_backup

    # Calls test_beat every 10 seconds
    # sender.add_periodic_task(3.0, debug_task, name="add every 10 seconds")
    sender.add_periodic_task(crontab(hour=18, minute=30, day_of_week="fri"), mysql_backup)
