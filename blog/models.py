from django.contrib.auth.models import User
from django.db import models

import markdown


class Post(models.Model):
    STATUS_ITEMS = (
        (1, '正常'),
        (2, '删除'),
        (3, '草稿'),
    )
    title = models.CharField(max_length=255, verbose_name='标题')
    owner = models.ForeignKey(User, verbose_name='作者', on_delete=models.PROTECT)
    category = models.ForeignKey('Category', verbose_name='分类', on_delete=models.PROTECT)
    tags = models.ManyToManyField('Tag', verbose_name='标签')
    desc = models.CharField(max_length=1024, blank=True, verbose_name='摘要')
    content = models.TextField(verbose_name='正文', help_text='正文仅支持Markdown语法')
    html = models.TextField(verbose_name='渲染后的内容', default='', help_text='正文仅支持Markdown语法')
    is_markdown = models.BooleanField(verbose_name='使用Markdown格式', default=True)
    status = models.PositiveIntegerField(default=1, choices=STATUS_ITEMS, verbose_name='状态')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def status_show(self):
        return '当前状态：{}'.format(self.get_status_display())

    status_show.short_description = '当前状态'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.is_markdown:
            config = {
                'codehilite': {
                    'use_pygments': False,
                    'css_class': 'prettyprint linenums',
                }
            }
            self.html = markdown.markdown(self.content, extensions=["codehilite"], extension_configs=config)
        return super(Post, self).save(*args, **kwargs)

    class Meta:
        verbose_name = verbose_name_plural = '  文章'
        ordering = ('-id',)


class Category(models.Model):
    STATUS_ITEMS = (
        (1, '正常'),
        (2, '删除'),
    )

    name = models.CharField(max_length=64, verbose_name='名称')
    status = models.PositiveIntegerField(default=1, choices=STATUS_ITEMS, verbose_name='状态')
    owner = models.ForeignKey(User, verbose_name='作者', on_delete=models.PROTECT)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    is_nav = models.BooleanField(default=0, verbose_name='是否置顶导航')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = ' 分类'


class Tag(models.Model):
    STATUS_ITEMS = (
        (1, '正常'),
        (2, '删除'),
    )

    name = models.CharField(max_length=64, verbose_name='名称')
    status = models.PositiveIntegerField(default=1, choices=STATUS_ITEMS, verbose_name='状态')
    owner = models.ForeignKey(User, verbose_name='作者', on_delete=models.PROTECT)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '标签'
