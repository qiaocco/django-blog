import mistune
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from django.db.models import F
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.functional import cached_property

from django_blog.utils import HighlightRenderer
from django_blog.signals import post_save_signal


class BaseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=1)


class BaseModel(models.Model):
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    objects = BaseManager()

    def get_full_url(self):
        site = Site.objects.get_current().domain
        url = f'https://{site}{self.get_absolute_url()}'
        return url

    class Meta:
        abstract = True


class Post(BaseModel):
    STATUS_ITEMS = (
        (1, '正常'),
        (2, '删除'),
        (3, '草稿'),
    )
    title = models.CharField(max_length=255, verbose_name='标题', db_index=True)
    owner = models.ForeignKey(User, verbose_name='作者', on_delete=models.PROTECT)
    content = models.TextField(verbose_name='正文', help_text='正文仅支持Markdown语法')
    html = models.TextField(verbose_name='渲染后的内容', default='', help_text='正文仅支持Markdown语法')
    is_markdown = models.BooleanField(verbose_name='使用Markdown格式', default=True)
    slug = models.SlugField(max_length=255, unique=True, verbose_name='Slug')
    category = models.ForeignKey('Category', verbose_name='分类', on_delete=models.PROTECT)
    tags = models.ManyToManyField('Tag', verbose_name='标签')
    desc = models.CharField(max_length=1024, blank=True, verbose_name='摘要')
    status = models.PositiveIntegerField(default=1, choices=STATUS_ITEMS, verbose_name='状态')
    pv = models.PositiveIntegerField(default=0, verbose_name='pv')
    uv = models.PositiveIntegerField(default=0, verbose_name='uv')

    def status_show(self):
        return '当前状态：{}'.format(self.get_status_display())

    status_show.short_description = '当前状态'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=(self.slug,))

    def increase_pv(self):
        return type(self).objects.filter(id=self.id).update(pv=F('pv') + 1)

    def increase_uv(self):
        return type(self).objects.filter(id=self.id).update(uv=F('uv') + 1)

    def save(self, *args, **kwargs):
        self.desc = self.desc or self.content[:140]
        self.slug = slugify(self.slug)
        if self.is_markdown:
            renderer = HighlightRenderer()
            self.html = mistune.markdown(self.content, renderer=renderer)
        post_save_signal.send(sender=self.__class__, id=self.id)
        return super(Post, self).save(*args, **kwargs)

    @cached_property
    def prev_post(self):
        return Post.objects.filter(id__gt=self.id, status=1).order_by('id').first()

    @cached_property
    def next_post(self):
        return Post.objects.filter(id__lt=self.id, status=1).order_by('id').first()

    class Meta:
        verbose_name = verbose_name_plural = '  文章'
        ordering = ('-id',)


class Category(BaseModel):
    STATUS_ITEMS = (
        (1, '正常'),
        (2, '删除'),
    )

    name = models.CharField(max_length=64, verbose_name='名称')
    status = models.PositiveIntegerField(default=1, choices=STATUS_ITEMS, verbose_name='状态')
    owner = models.ForeignKey(User, verbose_name='作者', on_delete=models.PROTECT)
    is_nav = models.BooleanField(default=0, verbose_name='是否置顶导航')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', args=(self.id,))

    class Meta:
        verbose_name = verbose_name_plural = ' 分类'


class Tag(BaseModel):
    STATUS_ITEMS = (
        (1, '正常'),
        (2, '删除'),
    )

    name = models.CharField(max_length=64, verbose_name='名称')
    status = models.PositiveIntegerField(default=1, choices=STATUS_ITEMS, verbose_name='状态')
    owner = models.ForeignKey(User, verbose_name='作者', on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tag', args=(self.id,))

    class Meta:
        verbose_name = verbose_name_plural = '标签'
