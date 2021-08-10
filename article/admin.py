from django.contrib import admin
from .models import *


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author_id', 'category_id', 'published', 'short_text']
    list_display_links = ['title']
    search_fields = ['title', 'text', ]


class CommentAdmin(admin.ModelAdmin):
    list_display = ['comment_author', 'article_id', 'comment_text', 'published']
    list_display_links = ['comment_author']
    search_fields = ['comment_author', 'article_id', 'comment_text']


admin.site.register(Category)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
