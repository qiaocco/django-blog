from django.urls import path

from .views import CategoryView, PostView, TagView, IndexView

app_name = 'blog'
urlpatterns = [
    path('', IndexView.as_view(), name='post_list'),
    path('category/<category_id>', CategoryView.as_view(), name='post_list'),
    path('tag/<tag_id>', TagView.as_view(), name='post_list'),
    # path('links', views.links, name='links'),
    path('<pk>', PostView.as_view(), name='post_detail'),
]
