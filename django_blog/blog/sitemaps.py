from django.contrib.sitemaps import Sitemap

from blog.models import Category, Post, Tag


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9
    protocol = 'https'

    def items(self):
        return Post.objects.filter(status=1)

    def lastmod(self, obj):
        return obj.updated_time