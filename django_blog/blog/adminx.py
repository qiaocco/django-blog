from django.urls import reverse
from django.utils.html import format_html

import xadmin
from django_blog.adminx import BaseOwnerAdmin
from xadmin.layout import Fieldset, Row

from .adminforms import PostAdminForm
from .models import Category, Post, Tag


class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm

    list_display = ('title', 'category', 'status_show', 'pv', 'uv', 'created_time', 'operator')
    list_filter = ('owner', 'category', 'status', 'created_time')
    search_fields = ('title', 'owner__username', 'category__name', 'desc')
    date_hierarchy = 'created_time'
    exclude = ('html', 'owner', 'pv', 'uv')

    # 编辑界面
    save_on_top = True

    form_layout = (
        Fieldset(
            '基础信息',
            'title',
            'slug',
            'desc',
            Row('category', 'status', 'is_markdown'),
            'content',
            'tags',
        )
    )

    def operator(self, obj):
        return format_html(
            '<a href={}>编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )

    operator.short_description = '操作'


class PostInline:
    fields = ('title', 'status')
    extra = 1
    model = Post


class CategoryAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time', 'is_nav', 'operator')
    list_filter = ('status', 'is_nav')
    search_fields = ('name',)
    inlines = (PostInline,)
    exclude = ('owner',)

    def operator(self, obj):
        return format_html(
            '<a href={}>编辑</a>',
            reverse('cus_admin:blog_category_change', args=(obj.id,))
        )

    operator.short_description = '操作'


class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time', 'operator')
    list_filter = ('status',)
    search_fields = ('name',)
    exclude = ('owner',)

    def operator(self, obj):
        return format_html(
            '<a href={}>编辑</a>',
            reverse('cus_admin:blog_tag_change', args=(obj.id,))
        )

    operator.short_description = '操作'


xadmin.site.register(Post, PostAdmin)
xadmin.site.register(Category, CategoryAdmin)
xadmin.site.register(Tag, TagAdmin)
