from .models import Article, Comment
from django import forms


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = {'title', 'category_id', 'text'}


class CommentForm(forms.Form):
    comment_text = forms.CharField(
        label='Текст комментария',
        widget=forms.TextInput
    )

