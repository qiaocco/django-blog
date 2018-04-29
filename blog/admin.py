from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import Post, Category, Tag
from django_blog.custom_site import custom_site


@admin.register(Post, site=custom_site)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'category', 'desc', 'status_show', 'created_time', 'operator')
    list_filter = ('owner', 'category', 'status', 'created_time')
    search_fields = ('title', 'owner__username', 'category__name', 'desc')
    show_full_result_count = False
    actions_on_top = True
    date_hierarchy = 'created_time'

    # 编辑界面
    # fields = (
    #     ('title', 'category'),
    #     'content',
    # )
    fieldsets = (
        ('基础配置', {
            'fields': (('title', 'category'), 'content', 'desc')
        }),
        ('高级配置', {
            'classes': ('collapse', 'addon'),
            'fields': ('tags',)
        })
    )
    filter_horizontal = ('tags',)

    def operator(self, obj):
        return format_html(
            '<a href={}>编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )

    operator.short_description = '操作'


@admin.register(Category, site=custom_site)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_time', 'is_nav', 'operator')
    list_filter = ('status', 'is_nav')
    search_fields = ('name',)

    def operator(self, obj):
        return format_html(
            '<a href={}>编辑</a>',
            reverse('cus_admin:blog_category_change', args=(obj.id,))
        )

    operator.short_description = '操作'


@admin.register(Tag, site=custom_site)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_time', 'operator')
    list_filter = ('status',)
    search_fields = ('name',)

    def operator(self, obj):
        return format_html(
            '<a href={}>编辑</a>',
            reverse('cus_admin:blog_tag_change', args=(obj.id,))
        )

    operator.short_description = '操作'
