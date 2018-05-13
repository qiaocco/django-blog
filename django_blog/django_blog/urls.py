"""django_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import re

import xadmin
from django.conf import settings
from django.urls import include, path, re_path
from django.views.static import serve
from django.views.decorators.cache import cache_page
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from xadmin.plugins import xversion

from blog.api import CategoryViewSet, PostViewSet, TagViewSet, UserViewSet
from blog.views import CategoryView, IndexView, PostView, TagView
from comment.views import CommentView

from .autocomplete import CategoryAutocomplete, TagAutocomplete

xadmin.autodiscover()

xversion.register_models()

router = routers.DefaultRouter()
router.register(r'post', PostViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'tag', TagViewSet)
router.register(r'user', UserViewSet)


def static(prefix, **kwargs):
    return [
        re_path(r'^%s(?P<path>.*)$' % re.escape(prefix.lstrip('/')), serve, kwargs=kwargs),
    ]


urlpatterns = [
                  path('', IndexView.as_view(), name='index'),
                  path('<int:pk>/', PostView.as_view(), name='post_detail'),
                  path('category/<int:category_id>/', cache_page(60 * 10)(CategoryView.as_view()), name='category'),
                  path('tag/<int:tag_id>/', TagView.as_view(), name='tag'),
                  path('comment/', CommentView.as_view(), name='comment'),

                  path('admin/', xadmin.site.urls),
                  path('category-autocomplete/', CategoryAutocomplete.as_view(), name='category_autocomplete'),
                  path('tag-autocomplete/', TagAutocomplete.as_view(), name='tag_autocomplete'),
                  path('api/docs/', include_docs_urls(title='My blog api docs')),
                  path('api/', include(router.urls)),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path(r'__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns