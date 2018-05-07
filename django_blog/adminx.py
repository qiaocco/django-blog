import xadmin
from xadmin.views import CommAdminView


class BaseOwnerAdmin:
    def get_list_queryset(self):
        request = self.request
        qs = super().get_list_queryset()
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

    def save_models(self):
        # import pdb;pdb.set_trace()
        if not self.org_obj:
            self.new_obj.owner = self.request.user
        return super(BaseOwnerAdmin, self).save_models()


class GlobalSetting(CommAdminView):
    site_title = '博客后台'
    site_footer = '@ pwer by jasonqiao36.cc'


xadmin.site.register(CommAdminView, GlobalSetting)
