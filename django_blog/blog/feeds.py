from django.contrib.syndication.views import Feed

from .models import Post


class LatestPostFeed(Feed):
    title = '最新文章'
    link = '/latest/feed'
    description = '展示5篇最新文章'

    def items(self):
        return Post.objects.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return 'desc'
