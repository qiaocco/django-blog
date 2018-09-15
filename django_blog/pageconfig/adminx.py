import xadmin
from common.adminx import BaseOwnerAdmin

from .models import Link, SideBar


class LinkAdmin(BaseOwnerAdmin):
    list_display = ('title', 'url', 'status', 'created_time', 'weigh')
    list_filter = ('status', 'created_time')
    search_fields = ('title', 'url')


class SideBarAdmin(BaseOwnerAdmin):
    list_display = ('title', 'display_type', 'created_time')
    list_filter = ('display_type', 'created_time')
    search_fields = ('title', 'content')


xadmin.site.register(Link, LinkAdmin)
xadmin.site.register(SideBar, SideBarAdmin)
