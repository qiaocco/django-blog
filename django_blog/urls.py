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
import xadmin

xadmin.autodiscover()
from xadmin.plugins import xversion

xversion.register_models()

from django.urls import path

from blog.views import CategoryView, PostView, TagView, IndexView
from comment.views import CommentView
from django_blog import adminx

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<int:pk>', PostView.as_view(), name='post_detail'),
    path('category/<int:category_id>', CategoryView.as_view(), name='category'),
    path('tag/<int:tag_id>', TagView.as_view(), name='tag'),
    path('comment/', CommentView.as_view(), name='comment'),

    path('admin/', xadmin.site.urls),
]
