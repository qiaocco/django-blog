from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.decorators.cache import cache_page
from rest_framework import routers
from rest_framework.documentation import include_docs_urls

from blog.api import CategoryViewSet, PostViewSet, TagViewSet, UserViewSet
from blog.feeds import LatestPostFeed
from blog.sitemaps import CategorySitemap, PostSitemap, TagSitemap
from blog.views import CategoryView, IndexView, PostView, SearchView, TagView
from comment.views import CommentView

router = routers.DefaultRouter()
router.register(r"post", PostViewSet)
router.register(r"category", CategoryViewSet)
router.register(r"tag", TagViewSet)
router.register(r"user", UserViewSet)

sitemaps = {"posts": PostSitemap, "categories": CategorySitemap, "tags": TagSitemap}

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path(
        "category/<int:category_id>/",
        cache_page(60 * 10)(CategoryView.as_view()),
        name="category",
    ),
    path("tag/<int:tag_id>/", TagView.as_view(), name="tag"),
    path("comment/", CommentView.as_view(), name="comment"),
    path("search/", SearchView.as_view(), name="search"),
    path("admin/", admin.site.urls),
    path("api/docs/", include_docs_urls(title="My blog api docs")),
    path("api/", include(router.urls)),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("latest/feed", LatestPostFeed(), name="feed"),
    # 放到最后, 防止匹配到其他url
    path("<slug:slug>/", PostView.as_view(), name="post_detail"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path(r"__debug__/", include(debug_toolbar.urls))] + urlpatterns
