from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .forms import UserRegistrationForm, LoginForm
from article.models import Category, Article
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required


# профиль пользователя
@login_required
def user_profile(request: HttpRequest) -> HttpResponse:
    categories = Category.objects.all()
    user = User.objects.get(username=request.user.username)
    user_articles = Article.objects.filter(author_id__username=user.username)
    return render(request, 'profile.html', {'user': user,
                                            'categories': categories,
                                            'articles': user_articles
                                            })


# вход пользователя
def user_login(request: HttpRequest) -> HttpResponse:
    categories = Category.objects.all()

    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse_lazy('profile'))
                else:
                    return HttpResponse('Неактивный аккаунт.')
            else:
                return HttpResponse('Неверный логин и/или пароль. Попробуйте ещё раз.')
    else:
        login_form = LoginForm()

    return render(request, 'registration/login.html', {'categories': categories,
                                                       'login_form': login_form
                                                       })


# выход пользователя
def user_logout(request: HttpRequest) -> HttpResponse:
    categories = Category.objects.all()
    return render(request, 'registration/logged_out.html', {'categories': categories})


# регистрация пользователя
def register(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password2'])
            new_user.save()
            return render(request, 'index.html')

    user_form = UserRegistrationForm()
    categories = Category.objects.all()
    return render(request, 'registration/register.html', {'user_form': user_form,
                                                          'categories': categories
                                                          })
