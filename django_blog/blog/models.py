import mistune
from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.functional import cached_property

from common.models import BaseModel
from common.signals import post_save_signal
from common.utils import HighlightRenderer


class Post(BaseModel):
    """
    博客文章
    """

    title = models.CharField(max_length=255, verbose_name="标题")
    content = models.TextField(verbose_name="正文", help_text="正文仅支持Markdown语法")
    html = models.TextField(
        verbose_name="渲染后的内容", default="", help_text="正文仅支持Markdown语法"
    )
    is_markdown = models.BooleanField(verbose_name="使用Markdown格式", default=True)
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Slug")
    category = models.ForeignKey(
        "Category", verbose_name="分类", on_delete=models.PROTECT
    )
    tag = models.ManyToManyField("Tag", verbose_name="标签")
    desc = models.CharField(max_length=1024, blank=True, verbose_name="摘要")
    pv = models.PositiveIntegerField(default=0, verbose_name="pv")
    uv = models.PositiveIntegerField(default=0, verbose_name="uv")

    class Meta:
        verbose_name = verbose_name_plural = "文章"
        ordering = ("-id",)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.desc = self.desc or self.content[:140]
        self.slug = slugify(self.slug)
        if self.is_markdown:
            renderer = HighlightRenderer()
            self.html = mistune.markdown(self.content, renderer=renderer)
        super().save(*args, **kwargs)
        post_save_signal.send(sender=self.__class__, id=self.id)

    def get_absolute_url(self):
        return reverse("post_detail", args=(self.slug,))

    @cached_property
    def prev_post(self):
        return (
            Post.objects.filter(id__gt=self.id, status=Post.STATUS_NORMAL)
            .order_by("id")
            .first()
        )

    @cached_property
    def next_post(self):
        return (
            Post.objects.filter(id__lt=self.id, status=Post.STATUS_NORMAL)
            .order_by("id")
            .first()
        )

    def status_show(self):
        return "当前状态：{}".format(self.get_status_display())

    status_show.short_description = "当前状态"


class Category(BaseModel):
    """文章分类"""

    name = models.CharField(max_length=64, verbose_name="名称")
    is_nav = models.BooleanField(default=0, verbose_name="是否置顶导航")

    class Meta:
        verbose_name = verbose_name_plural = "分类"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category", args=(self.id,))


class Tag(BaseModel):
    """文章标签"""

    name = models.CharField(max_length=64, verbose_name="名称")

    class Meta:
        verbose_name = verbose_name_plural = "标签"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("tag", args=(self.id,))
