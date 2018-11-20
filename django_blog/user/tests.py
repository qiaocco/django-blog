import os

from django.contrib.auth import get_user_model
from django.test import Client, RequestFactory, TestCase


class UserTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

        profile = os.environ.get("DJANGO_BLOG_PROFILE", "test")
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.{}".format(profile))

    def test_user(self):
        get_user_model().objects.get_or_create(username="jason", email="jasonqiao36@gmail.com")
        user = get_user_model().objects.first()
        assert user.username == "jason"
