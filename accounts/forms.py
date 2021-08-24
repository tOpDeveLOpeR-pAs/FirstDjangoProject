from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms
from article.models import Article, Category


# вход пользователей
class LoginForm(forms.Form):
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput
    )


# регистрация пользователей
class UserRegistrationForm(forms.Form):
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput
    )

    email = forms.EmailField(
        label="Почтовый ящик",
        widget=forms.EmailInput
    )

    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label="Повторите пароль",
        widget=forms.PasswordInput
    )

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password2']


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = {'title', 'category_id', 'text'}


