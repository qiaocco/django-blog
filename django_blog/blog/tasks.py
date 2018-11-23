from celery.task import Task
from celery.utils.log import get_task_logger
from celery.worker.request import Request
from django.db.models import F

from django_blog import celery_app
from .models import Post

logger = get_task_logger(__name__)


class MyRequest(Request):
    def on_success(self, failed__retval__runtime, **kwargs):
        super(MyRequest, self).on_success(failed__retval__runtime, **kwargs)
        logger.info(f'Execute success: {self.task.name}')

    def on_failure(self, exc_info, send_failed_event=True, return_ok=False):
        super(MyRequest, self).on_failure(exc_info, send_failed_event=send_failed_event, return_ok=return_ok)
        logger.info(f'Execute fail: {self.task.name}')


class MyTask(Task):
    Request = MyRequest


@celery_app.task(base=MyTask)
def increase_pv_uv(pk):
    return Post.objects.filter(pk=pk).update(pv=F("pv") + 1, uv=F("uv") + 1)


@celery_app.task(base=MyTask)
def increase_pv(pk):
    return Post.objects.filter(pk=pk).update(pv=F("pv") + 1)


@celery_app.task(base=MyTask)
def increase_uv(pk):
    return Post.objects.filter(pk=pk).update(uv=F("uv") + 1)
