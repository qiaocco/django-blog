from django.contrib.auth.models import User
from django.db import connection
from django.db.models.functions import Lower
from django.test import TestCase
from django.test.utils import override_settings

from .models import Category, Post


class TestCategory(TestCase):
    def setUp(self):
        user = User.objects.create_user('jason', 'wuxia64@qq.com', 'password')
        for i in range(10):
            category_name = 'Cat_{}'.format(i)
            Category.objects.create(name=category_name, owner=user)

    @override_settings(DEBUG=True)
    def test_filter(self):
        from django.db.models import Max, Count
        categories = Category.objects.defer('name')
        print(categories)
        print(connection.queries)
