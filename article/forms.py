from django import forms
from .models import Comment


class CommentForm(forms.Form):
    comment_text = forms.CharField(
        label='Текст комментария',
        widget=forms.TextInput
    )

