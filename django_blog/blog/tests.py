from django.contrib.auth.models import User
from django.db import connection
from django.test import Client, RequestFactory, TestCase
from django.test.utils import override_settings

from blog.models import Category


class TestCategory(TestCase):
    def setUp(self):
        user = User.objects.create_user('jason', 'wuxia64@qq.com', 'password')
        for i in range(10):
            category_name = 'Cat_{}'.format(i)
            Category.objects.create(name=category_name, owner=user)

    @override_settings(DEBUG=True)
    def test_filter(self):
        categories = Category.objects.defer('name')
        print(categories)
        print(connection.queries)


class PostTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    def test_validate_post(self):
        from django.contrib.auth import get_user_model

        get_user_model().objects.get_or_create(
            username='jason',
            email='jasonqiao36@gmail.com'
        )
        user = get_user_model().objects.first()
        assert user.username == 'jason'
        # category = Category.objects.all()
