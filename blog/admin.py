from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from django_blog.custom_site import custom_site

from .adminforms import PostAdminForm
from .models import Category, Post, Tag


@admin.register(Post, site=custom_site)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm

    list_display = ('title', 'category', 'status_show', 'pv', 'uv', 'created_time', 'operator')
    list_filter = ('owner', 'category', 'status', 'created_time')
    search_fields = ('title', 'owner__username', 'category__name', 'desc')
    date_hierarchy = 'created_time'

    # 编辑界面
    save_on_top = True
    fields = (
        ('title', 'category'),
        'desc',
        'status',
        ('content', 'is_markdown'),
        'html',
        'tags',
    )

    def operator(self, obj):
        return format_html(
            '<a href={}>编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )

    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        super().save_model(request, obj, form, change)


class PostInline(admin.TabularInline):
    fields = ('title', 'status')
    extra = 1
    model = Post


@admin.register(Category, site=custom_site)
class CategoryAdmin(admin.ModelAdmin):
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

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        super().save_model(request, obj, form, change)


@admin.register(Tag, site=custom_site)
class TagAdmin(admin.ModelAdmin):
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

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        super().save_model(request, obj, form, change)
