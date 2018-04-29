from django.contrib.auth.models import User
from django.db import models


class Link(models.Model):
    STATUS_ITEMS = (
        (1, '正常'),
        (2, '删除'),
    )
    title = models.CharField(max_length=64, verbose_name='网站名称')
    url = models.URLField(verbose_name='链接')
    owner = models.CharField(max_length=64, verbose_name='作者')
    status = models.PositiveIntegerField(default=1, choices=STATUS_ITEMS, verbose_name='状态')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    weigh = models.PositiveIntegerField(default=1, choices=zip(range(1, 6), range(1, 6)),
                                        verbose_name='权重',
                                        help_text='权重越高，展示顺序越靠前')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = verbose_name_plural = '友链'


class SideBar(models.Model):
    DISPLAY_ITEMS = (
        (1, '最新文章'),
        (2, '最热文章'),
        (3, '最近评论'),
        (4, '内容'),
    )
    title = models.CharField(max_length=64, verbose_name='标题')
    display_type = models.PositiveIntegerField(default=1, choices=DISPLAY_ITEMS, verbose_name='展示类型')
    content = models.CharField(max_length=512, blank=True, verbose_name='内容', help_text='如果设置的不是ＨＴＭＬ类型，可为空')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    owner = models.ForeignKey(User, verbose_name='作者', on_delete=models.PROTECT)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = verbose_name_plural = '侧栏'
