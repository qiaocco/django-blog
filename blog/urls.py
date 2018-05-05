from django.urls import path

from .views import CategoryView, PostView, TagView, IndexView

app_name = 'blog'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('category/<int:category_id>', CategoryView.as_view(), name='category'),
    path('tag/<int:tag_id>', TagView.as_view(), name='tag'),
    # path('links', views.links, name='links'),
    path('<int:pk>', PostView.as_view(), name='post_detail'),
]
