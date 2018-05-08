from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 10:
            raise forms.ValidationError('内容少于10个字符啦！')
        return content

    class Meta:
        model = Comment
        fields = ['target', 'nickname', 'email', 'website', 'content']
