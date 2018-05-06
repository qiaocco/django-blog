from django.shortcuts import redirect
from django.views.generic import TemplateView

from .models import Comment
from .forms import CommentForm


class CommentShowMixin:
    def get_comments(self):
        target = self.request.path
        comments = Comment.objects.filter(target=target).filter(status=1)
        return comments

    def get_context_data(self, **kwargs):
        kwargs.update({
            'comment_form': CommentForm,
            'comment_list': self.get_comments()
        })
        return super(CommentShowMixin, self).get_context_data(**kwargs)


class CommentView(TemplateView):
    template_name = 'comment/result.html'

    def post(self, request, *args, **kwargs):
        target = self.request.POST.get('target')
        comment_form = CommentForm(request.POST)
        comment_form.target = target

        if comment_form.is_valid():
            comment_form.save()
            return redirect(target)
        else:
            context = {
                'form': comment_form,
                'target': target,
            }
            return self.render_to_response(context)
