from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from django_blog.custom_site import custom_site

from .models import Comment


@admin.register(Comment, site=custom_site)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('target', 'nickname', 'email', 'created_time', 'operator')
    list_filter = ('target', 'created_time')
    search_fields = ('content', 'post__title')

    def operator(self, obj):
        return format_html(
            '<a href={}>编辑</a>',
            reverse('cus_admin:comment_comment_change', args=(obj.id,))
        )

    operator.short_description = '操作'
