from django.shortcuts import render
from django.views.generic import TemplateView


class CommentView(TemplateView):
    template_name = 'comment/result.html'

    def get(self, request, *args, **kwargs):
        return super(CommentView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        target = request.POST.get('target')
        context = {
            'succeed': True
        }
        return self.render_to_response(context)
