from django.db import models

from blog.models import Post


class Comment(models.Model):
    post = models.ForeignKey(Post, verbose_name='文章', on_delete=models.PROTECT)
    nickname = models.CharField(max_length=64, verbose_name='用户名')
    email = models.EmailField(verbose_name='邮箱')
    website = models.URLField(verbose_name='网站地址')
    content = models.CharField(max_length=2000, verbose_name='内容')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return '评论：{}'.format(self.post)

    class Meta:
        verbose_name = verbose_name_plural = '评论'
