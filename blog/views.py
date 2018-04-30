from django.shortcuts import render, Http404
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView

from .models import Post, Tag, Category
from config.models import SideBar
from comment.models import Comment


class CommonMixin(object):
    def get_context_data(self):
        categories = Category.objects.filter(status=1)
        nav_cates = []
        cates = []
        for cate in categories:
            if cate.is_nav:
                nav_cates.append(cate)
            else:
                cates.append(cate)

        sidebars = SideBar.objects.filter(status=1)

        recently_posts = Post.objects.filter(status=1)[:10]
        # hot_posts = Post.objects.filter(status=1)[:10]
        recently_comments = Comment.objects.filter(status=1)[:10]

        context = {
            'nav_cates': nav_cates,
            'cates': cates,
            'sidebars': sidebars,
            'recently_posts': recently_posts,
            'recently_comments': recently_comments,
        }
        return super(CommonMixin, self).get_context_data(**context)


class BasePostsView(CommonMixin, ListView):
    model = Post
    template_name = 'blog/post-list.html'
    context_object_name = 'posts'
    paginate_by = 3


class IndexView(BasePostsView):
    pass


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


def get_common_context():
    categories = Category.objects.filter(status=1)
    nav_cates = []
    cates = []
    for cate in categories:
        if cate.is_nav:
            nav_cates.append(cate)
        else:
            cates.append(cate)

    sidebars = SideBar.objects.filter(status=1)

    recently_posts = Post.objects.filter(status=1)[:10]
    # hot_posts = Post.objects.filter(status=1)[:10]
    recently_comments = Comment.objects.filter(status=1)[:10]

    context = {
        'nav_cates': nav_cates,
        'cates': cates,
        'sidebars': sidebars,
        'recently_posts': recently_posts,
        'recently_comments': recently_comments,
    }
    return context


def post_list(request, category_id=None, tag_id=None):
    page = request.GET.get('page', 1)
    per_page = 5
    queryset = Post.objects.all()
    if category_id:
        queryset = Post.objects.filter(category_id=category_id)
    elif tag_id:
        try:
            tag = Tag.objects.get(pk=tag_id)
        except Tag.DoesNotExist:
            queryset = []
        else:
            queryset = tag.post_set.all()

    paginator = Paginator(queryset, per_page)
    posts = paginator.get_page(page)

    context = {
        'posts': posts,
    }
    common_context = get_common_context()
    context.update(common_context)
    return render(request, 'blog/post-list.html', context=context)


def post_detail(request, post_id=None):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        raise Http404('Post does not exist')

    context = {
        'post': post
    }
    common_context = get_common_context()
    context.update(common_context)
    return render(request, 'blog/post-detail.html', context=context)
