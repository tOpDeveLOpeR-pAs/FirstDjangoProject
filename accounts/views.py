from django.contrib.auth import authenticate, login, get_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpRequest, HttpResponse
from article.models import Category
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import *


# профиль пользователя
@login_required
def user_profile(request: HttpRequest) -> HttpResponse:
    categories = Category.objects.all()
    user = User.objects.get(username=request.user.username)
    user_articles = Article.objects.filter(author_id__username=user.username)
    return render(request, 'accounts/profile.html', {'user': user,
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
class UserLogoutView(LogoutView):
    categories = Category.objects.all()
    extra_context = {'categories': categories}
    next_page = 'index'


# регистрация пользователя
def register(request: HttpRequest) -> HttpResponse:
    categories = Category.objects.all()
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            cd = user_form.cleaned_data
            new_user = User.objects.create_user(cd['username'],
                                                cd['email'],
                                                cd['password'])
            new_user.save()
            return redirect(reverse_lazy('login'))

    user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form,
                                                          'categories': categories
                                                          })


# добавление статьи
@login_required
def add_article(request: HttpRequest) -> HttpResponse:
    categories = Category.objects.all()
    if request.method == "POST":
        article_form = ArticleForm(request.POST)
        if article_form.is_valid():
            article = Article()
            article.category_id = article_form.cleaned_data['category_id']
            article.title = article_form.cleaned_data['title']
            article.text = article_form.cleaned_data['text']
            article.author_id = get_user(request)

            article.save()
            return redirect('by_category', category_id=article.category_id)
        else:
            render(request, 'accounts/create_article.html', {'form': article_form,
                                                             'categories': categories
                                                             })
    article_form = ArticleForm()
    return render(request, 'accounts/create_article.html', {'form': article_form,
                                                            'categories': categories
                                                            })


@login_required
def update_article(request: HttpRequest, article_id: int) -> HttpResponse:
    categories = Category.objects.all()
    article = Article.objects.get(id=article_id)

    if request.method == "POST":
        article_form = ArticleForm(request.POST)
        if article_form.is_valid():
            article.category_id = article_form.cleaned_data['category_id']
            article.title = article_form.cleaned_data['title']
            article.text = article_form.cleaned_data['text']

            article.save()
            return redirect('by_category', category_id=article.category_id)
        else:
            render(request, 'accounts/update_article.html', {'form': article_form,
                                                             'categories': categories,
                                                             })

    article_form = ArticleForm(initial={'title': article.title,
                                        'category_id': article.category_id,
                                        'text': article.text
                                        })
    return render(request, 'accounts/update_article.html', {'form': article_form,
                                                            'categories': categories
                                                            })


@login_required()
def delete_article(request: HttpRequest, article_id: int) -> HttpResponse:
    article = Article.objects.get(pk=article_id)
    article.delete()
    return redirect('profile')



