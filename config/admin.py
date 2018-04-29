from django.contrib import admin

from django_blog.custom_site import custom_site

from .models import Link, SideBar


@admin.register(Link, site=custom_site)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'status', 'created_time', 'weigh')
    list_filter = ('status', 'created_time')
    search_fields = ('title', 'url')


@admin.register(SideBar, site=custom_site)
class SideBarAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_type', 'created_time')
    list_filter = ('display_type', 'created_time')
    search_fields = ('title', 'content')
