from django.urls import path
from .views import *


urlpatterns = [
    path('<str:category_id>/<int:article_id>/add_comment/', add_comment, name='add_comment'),
    path('<str:category_id>/<int:article_id>/', ArticleDetailView.as_view(), name='by_article'),
    path('<str:category_id>/', CategoryListView.as_view(), name='by_category'),
    path('', IndexListView.as_view(), name='index'),
]
