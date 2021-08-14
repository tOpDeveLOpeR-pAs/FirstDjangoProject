from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.core import validators
from django.urls import reverse


# Основные классы | Категория статей | Статьи | Комментарии
class Category(models.Model):
    name = models.CharField(max_length=30, db_index=True, verbose_name='Название')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Article(models.Model):
    category_id = models.ForeignKey(Category, null=True, on_delete=models.PROTECT, verbose_name='Категория')
    author_id = models.ForeignKey(User, null=True, on_delete=models.CASCADE, verbose_name='Автор')

    title = models.CharField(max_length=100, blank=True, verbose_name='Заголовок')
    published = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Дата публикации')
    text = models.TextField(verbose_name='Текст статьи', blank=True,
                            validators=[validators.MinLengthValidator(100),
                                        validators.MaxLengthValidator(100000),
                                        ])

    def get_absolute_url(self):
        return reverse('by_article', kwargs={'category_id': self.category_id, 'article_id': self.pk})

    def __str__(self):
        return self.title

    @admin.display
    def short_text(self):
        return self.text[:400] + ' ...'

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        unique_together = ('title', 'published')
        get_latest_by = '-published'
        ordering = ['-published']


class Comment(models.Model):
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья')

    comment_author = models.CharField(max_length=50, null=True, verbose_name='Автор комментария')
    comment_text = models.CharField(max_length=200, null=True, verbose_name='Текст комментария')
    published = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-published']

    def __str__(self):
        return self.comment_author
