from django.contrib.sites.models import Site
from django.db import models


class BaseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=BaseModel.STATUS_NORMAL)


class BaseModel(models.Model):
    STATUS_DELETE = 0
    STATUS_NORMAL = 1
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_DELETE, '删除'),
        (STATUS_NORMAL, '正常'),
        (STATUS_DRAFT, '草稿'),
    )

    status = models.PositiveIntegerField(choices=STATUS_ITEMS, default=STATUS_NORMAL, verbose_name='状态')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    objects = BaseManager()

    def get_full_url(self):
        site = Site.objects.get_current().domain
        url = 'https://{site}{obsolute_url}'.format(site=site, obsolute_url=self.get_absolute_url())
        return url

    class Meta:
        abstract = True
