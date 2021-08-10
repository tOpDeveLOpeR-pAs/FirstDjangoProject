from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .models import *
from .forms import ArticleForm, CommentForm
from typing import Any


def index(request: HttpRequest) -> HttpResponse:
    latest_articles_list = Article.objects.all()[:5]
    categories = Category.objects.all()
    return render(request, 'index.html', context={'articles': latest_articles_list,
                                                  'categories': categories,
                                                  })


def by_article(request: HttpRequest, category_id: str, article_id: int) -> HttpResponse:
    current_article = get_object_or_404(Article, pk=article_id)
    current_comments = Comment.objects.filter(article_id=article_id)
    categories = Category.objects.all()
    comment_form = CommentForm
    return render(request, 'by_article.html', context={'article': current_article,
                                                       'comments': current_comments,
                                                       'categories': categories,
                                                       'form': comment_form
                                                       })


def by_category(request: HttpRequest, category_id: str) -> HttpResponse:
    category = get_object_or_404(Category, name=category_id)
    categories = Category.objects.all()
    current_articles = Article.objects.filter(category_id__name=category_id)
    return render(request, 'by_category.html', context={'category': category,
                                                        'categories': categories,
                                                        'articles': current_articles,
                                                        })


@login_required()
def add_comment(request: HttpRequest, category_id: str, article_id: int):
    comment_form = CommentForm(request.POST)
    article = get_object_or_404(Article, id=article_id)

    if comment_form.is_valid():
        comment = Comment()
        comment.article_id = article
        comment.comment_author = auth.get_user(request)
        comment.comment_text = comment_form.cleaned_data['comment_text']
        comment.save()

    return redirect(article.get_absolute_url())


@login_required
def add_article(request: HttpRequest) -> HttpResponse:
    categories = Category.objects.all()
    article_form = ArticleForm(request.POST)

    if article_form.is_valid():
        article = Article()
        article.category_id = article_form.cleaned_data['category_id']
        article.title = article_form.cleaned_data['title']
        article.text = article_form.cleaned_data['text']
        article.author_id = auth.get_user(request)

        article.save()
        return redirect(reverse_lazy('index'))

    return render(request, 'create_article.html', {'form': article_form,
                                                   'categories': categories
                                                   })


