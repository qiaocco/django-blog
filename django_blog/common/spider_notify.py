import requests
from django.conf import settings
from django.contrib.sitemaps import ping_google


class SpiderNotify:
    @staticmethod
    def notify_baidu(url):
        try:
            requests.post(settings.BAIDU_NOTIFY_URL, data=url)
        except Exception as e:
            print(e)

    @staticmethod
    def notify_google():
        try:
            ping_google(sitemap_url="/sitemap.xml")
        except Exception as e:
            print(e)
