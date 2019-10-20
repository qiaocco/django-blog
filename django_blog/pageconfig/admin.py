from django.contrib import admin

from .models import Link, SideBar


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ("title", "url", "status", "created_time", "weigh")
    list_filter = ("status", "created_time")
    search_fields = ("title", "url")


@admin.register(SideBar)
class SideBarAdmin(admin.ModelAdmin):
    list_display = ("title", "display_type", "created_time")
    list_filter = ("display_type", "created_time")
    search_fields = ("title", "content")
