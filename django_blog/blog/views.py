from django.core.cache import cache
from django.db.models import Q
from django.views.generic import DetailView, ListView

from comment.models import Comment
from comment.views import CommentShowMixin
from pageconfig.models import Link, SideBar

from .models import Category, Post
from .tasks import increase_pv, increase_pv_uv, increase_uv


class CommonViewMixin:
    def get_navs(self):
        categories = Category.objects.all()

        nav_cates = []
        cates = []
        for cate in categories:
            if cate.is_nav:
                nav_cates.append(cate)
            else:
                cates.append(cate)
        return {"nav_cates": nav_cates, "cates": cates}

    def get_sidebars(self):
        sidebars = SideBar.objects.all()

        recently_posts = Post.objects.all()[:10]
        hot_posts = Post.objects.order_by("-pv")[:10]
        recently_comments = Comment.objects.all()[:10]
        links = Link.objects.all()
        htmls = SideBar.objects.filter(display_type=SideBar.DISPLAY_HTML)

        return {
            "sidebars": sidebars,
            "recently_posts": recently_posts,
            "hot_posts": hot_posts,
            "recently_comments": recently_comments,
            "links": links,
            "htmls": htmls,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_navs())
        context.update(self.get_sidebars())
        context.update({"query": self.request.GET.get("query")})
        return context


class IndexView(CommonViewMixin, ListView):
    queryset = Post.objects.select_related("category").prefetch_related("tag")
    paginate_by = 10
    template_name = "blog/post-list.html"
    context_object_name = "posts"


class CategoryView(IndexView):
    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get("category_id")
        return queryset.filter(category_id=category_id)


class TagView(IndexView):
    def get_queryset(self):
        queryset = super().get_queryset()
        tag_id = self.kwargs.get("tag_id")
        return queryset.filter(tag__id=tag_id)


class PostView(CommonViewMixin, CommentShowMixin, DetailView):
    model = Post
    template_name = "blog/post-detail.html"
    context_object_name = "post"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.pv_uv()
        return response

    def get_context_data(self, **kwargs):
        kwargs.update(
            {"prev_post": self.object.prev_post, "next_post": self.object.next_post}
        )
        return super().get_context_data(**kwargs)

    def pv_uv(self):
        need_increase_pv = False
        need_increase_uv = False
        uid = self.request.uid

        pv_key = f"pv:{uid}:{self.request.path}"
        if not cache.get(pv_key):
            need_increase_pv = True
            cache.set(pv_key, 1, 1 * 1)  # 1min有效

        uv_key = f"uv:{uid}:{self.request.path}"
        if not cache.get(uv_key):
            need_increase_uv = True
            cache.set(uv_key, 1, 24 * 60 * 60)  # 24h有效

        if need_increase_pv and need_increase_uv:
            increase_pv_uv.delay(self.object.id)
        elif need_increase_pv:
            increase_pv.delay(self.object.id)
        elif need_increase_uv:
            increase_uv.delay(self.object.id)


class SearchView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"query": self.request.GET.get("query", "")})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("query")
        if not query:
            return queryset
        return queryset.filter(Q(title__icontains=query) | Q(desc__icontains=query))
