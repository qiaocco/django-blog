from django.contrib.sitemaps import ping_google
from django.conf import settings

import requests


class SpiderNotify:
    @staticmethod
    def notify_baidu(urls):
        try:
            data = '\n'.join(urls)
            result = requests.post(settings.BAIDU_NOTIFY_URL, data=data)
        except Exception as e:
            print(e)

    @staticmethod
    def notify_google(url):
        try:
            ping_google(url)
        except Exception as e:
            print(e)
