from django.contrib import admin

from .models import Post, Category, Tag
from django_blog.custom_site import custom_site


@admin.register(Post, site=custom_site)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'category', 'desc', 'status', 'created_time')
    list_filter = ('owner', 'category', 'status', 'created_time')
    search_fields = ('title', 'owner__username', 'category__name', 'desc')
    save_on_top = True
    show_full_result_count = False


@admin.register(Category, site=custom_site)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag, site=custom_site)
class TagAdmin(admin.ModelAdmin):
    pass
