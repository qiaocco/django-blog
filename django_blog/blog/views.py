from django.core.cache import cache
from django.views.generic import DetailView, ListView

from comment.models import Comment
from comment.views import CommentShowMixin
from config.models import Link, SideBar

from .models import Category, Post, Tag


class CommonMixin:
    def get_category_context(self):
        categories = Category.objects.all()

        nav_cates = []
        cates = []
        for cate in categories:
            if cate.is_nav:
                nav_cates.append(cate)
            else:
                cates.append(cate)
        return {
            'nav_cates': nav_cates,
            'cates': cates,
        }

    def get_context_data(self, **kwargs):
        sidebars = SideBar.objects.all()

        recently_posts = Post.objects.all()[:10]
        hot_posts = Post.objects.order_by('-pv')[:10]
        recently_comments = Comment.objects.all()[:10]
        links = Link.objects.all()
        htmls = SideBar.objects.filter(display_type=1)

        kwargs.update({
            'sidebars': sidebars,
            'recently_posts': recently_posts,
            'hot_posts': hot_posts,
            'recently_comments': recently_comments,
            'links': links,
            'htmls': htmls,
        })
        kwargs.update(self.get_category_context())
        return super().get_context_data(**kwargs)


class BasePostsView(CommonMixin, ListView):
    model = Post
    template_name = 'blog/post-list.html'
    context_object_name = 'posts'
    paginate_by = 3


class IndexView(BasePostsView):
    queryset = Post.objects.select_related('category').prefetch_related('tags')
    paginate_by = 10
    allow_empty = True

    def get_queryset(self):
        query = self.request.GET.get('query')
        qs = super().get_queryset()
        if not query:
            return qs
        return qs.filter(title__icontains=query)

    def get_context_data(self, **kwargs):
        query = self.request.GET.get('query')
        return super().get_context_data(query=query)


class CategoryView(BasePostsView):
    def get_queryset(self):
        qs = super().get_queryset()
        cat_id = self.kwargs.get('category_id')
        qs = qs.filter(category_id=cat_id)
        return qs


class TagView(BasePostsView):
    def get_queryset(self):
        tag_id = self.kwargs.get('tag_id')
        try:
            tag = Tag.objects.get(pk=tag_id)
        except Tag.DoesNotExist:
            return []

        posts = tag.post_set.all()
        return posts


class PostView(CommonMixin, CommentShowMixin, DetailView):
    queryset = Post.objects.select_related('owner')
    template_name = 'blog/post-detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        response = super(PostView, self).get(request, *args, **kwargs)
        self.pv_uv()
        return response

    def get_context_data(self, **kwargs):
        kwargs.update({
            'prev_post': self.object.prev_post,
            'next_post': self.object.next_post,
        })
        return super().get_context_data(**kwargs)

    def pv_uv(self):
        sessionid = self.request.COOKIES.get('sessionid')
        if not sessionid:
            return

        pv_key = 'pv:{}:{}'.format(sessionid, self.request.path)
        if not cache.get(pv_key):
            self.object.increase_pv()
            cache.set(pv_key, 1, 30)

        uv_key = 'uv:{}:{}'.format(sessionid, self.request.path)
        if not cache.get(uv_key):
            self.object.increase_uv()
            cache.set(uv_key, 1, 60 * 60 * 24)
