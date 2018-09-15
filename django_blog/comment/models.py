from common.models import BaseModel
from django.db import models


class Comment(BaseModel):
    """用户评论"""

    target = models.CharField(max_length=200, null=True, verbose_name='评论目标')
    nickname = models.CharField(max_length=64, verbose_name='用户名')
    email = models.EmailField(verbose_name='邮箱')
    website = models.URLField(verbose_name='网站地址')
    content = models.CharField(max_length=2000, verbose_name='内容')

    class Meta:
        verbose_name = verbose_name_plural = '评论'

    def __str__(self):
        return '评论：{}'.format(self.nickname)
