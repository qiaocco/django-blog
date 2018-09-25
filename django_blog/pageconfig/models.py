from django.conf import settings
from django.db import models

from common.models import BaseModel


class Link(BaseModel):
    """友链"""

    title = models.CharField(max_length=64, verbose_name='网站名称')
    url = models.URLField(verbose_name='链接')
    owner = models.CharField(max_length=64, verbose_name='网站作者')
    weigh = models.PositiveIntegerField(
        default=1,
        choices=zip(range(1, 6), range(1, 6)),
        verbose_name='权重',
        help_text='权重越高，展示顺序越靠前'
    )

    class Meta:
        verbose_name = verbose_name_plural = '友链'

    def __str__(self):
        return self.title


class SideBar(BaseModel):
    """侧边栏"""

    DISPLAY_ITEMS = (
        (1, 'HTML'),
        (2, '最新文章'),
        (3, '最热文章'),
        (4, '最近评论'),
        (5, '友链'),
    )
    title = models.CharField(max_length=64, verbose_name='标题')
    display_type = models.PositiveIntegerField(default=1, choices=DISPLAY_ITEMS, verbose_name='展示类型')
    content = models.CharField(max_length=512, blank=True, verbose_name='内容', help_text='如果设置的不是HTML类型，可为空')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='作者', on_delete=models.PROTECT)

    class Meta:
        verbose_name = verbose_name_plural = '侧边栏'
        ordering = ('display_type',)

    def __str__(self):
        return self.title
