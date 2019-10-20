from django.contrib import admin


class BaseOwnerAdmin(admin.ModelAdmin):
    def get_list_queryset(self):
        request = self.request
        qs = super().get_list_queryset()
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

    def save_models(self):
        if not self.org_obj:
            self.new_obj.owner = self.request.user
        return super(BaseOwnerAdmin, self).save_models()


class MyAdminSite(admin.AdminSite):
    site_title = "博客后台"
    site_footer = "power by jasonqiao36.cc"


admin_site = MyAdminSite(name="myadmin")
admin_site.register()
