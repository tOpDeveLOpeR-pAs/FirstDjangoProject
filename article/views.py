from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import *
from .forms import CommentForm


class IndexListView(ListView):
    template_name = 'index.html'
    context_object_name = 'articles'
    ordering = '-published'
    paginate_by = 5

    def get_queryset(self):
        return Article.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'by_article.html'

    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.kwargs['article_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(article_id=self.kwargs['article_id'])
        context['categories'] = Category.objects.all()
        context['form'] = CommentForm

        return context


class CategoryListView(ListView):
    template_name = 'by_category.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects.filter(category_id__name=self.kwargs['category_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, name=self.kwargs['category_id'])
        context['categories'] = Category.objects.all()

        return context


@login_required()
def add_comment(request: HttpRequest, category_id: str, article_id: int) -> HttpResponse:
    comment_form = CommentForm(request.POST)
    article = get_object_or_404(Article, id=article_id)

    if comment_form.is_valid():
        comment = Comment()
        comment.article_id = article
        comment.comment_author = get_user(request)
        comment.comment_text = comment_form.cleaned_data['comment_text']
        comment.save()

    return redirect(article.get_absolute_url())



