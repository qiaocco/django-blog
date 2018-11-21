from django.db.models import F

from django_blog import celery_app

from .models import Post


@celery_app.task
def increase_pv_uv(pk):
    return Post.objects.filter(pk=pk).update(pv=F("pv") + 1, uv=F("uv") + 1)


@celery_app.task
def increase_pv(pk):
    return Post.objects.filter(pk=pk).update(pv=F("pv") + 1)


@celery_app.task
def increase_uv(pk):
    return Post.objects.filter(pk=pk).update(uv=F("uv") + 1)
