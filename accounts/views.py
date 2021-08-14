from django.contrib.auth import authenticate, login, get_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from article.models import Category, Article
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse
from .forms import ArticleForm, UserRegistrationForm, LoginForm


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
            render(request, 'create_article.html', {'form': article_form,
                                                    'categories': categories
                                                    })
    article_form = ArticleForm()
    return render(request, 'create_article.html', {'form': article_form,
                                                   'categories': categories
                                                   })


class ArticleCreateView(LoginRequiredMixin, CreateView):
    template_name = 'create_article.html'
    form_class = ArticleForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def get_success_url(self):
        form_kwargs = self.get_form_kwargs()
        category_id = Category.objects.get(pk=form_kwargs['data']['category_id']).name
        return reverse('by_category', kwargs={'category_id': category_id})
