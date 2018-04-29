from django.contrib.admin import AdminSite


class CustomSite(AdminSite):
    site_header = '博客管理后台'
    site_title = '博客管理后台'


custom_site = CustomSite(name='cus_site')
