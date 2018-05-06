from django.views.generic import ListView, DetailView

from .models import Post, Tag, Category
from config.models import SideBar
from comment.models import Comment
from config.models import Link


class CommonMixin(object):
    def get_category_context(self):
        categories = Category.objects.filter(status=1)

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
        sidebars = SideBar.objects.filter(status=1)

        recently_posts = Post.objects.filter(status=1)[:10]
        # hot_posts = Post.objects.filter(status=1)[:10]
        recently_comments = Comment.objects.filter(status=1)[:10]
        links = Link.objects.filter(status=1)

        kwargs.update({
            'sidebars': sidebars,
            'recently_posts': recently_posts,
            'recently_comments': recently_comments,
            'links': links,
        })
        kwargs.update(self.get_category_context())
        return super(CommonMixin, self).get_context_data(**kwargs)


class BasePostsView(CommonMixin, ListView):
    model = Post
    template_name = 'blog/post-list.html'
    context_object_name = 'posts'
    paginate_by = 3


class IndexView(BasePostsView):
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
        return super(IndexView, self).get_context_data(query=query)


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


class PostView(CommonMixin, DetailView):
    model = Post
    template_name = 'blog/post-detail.html'
    context_object_name = 'post'

    def post(self):
        pass
