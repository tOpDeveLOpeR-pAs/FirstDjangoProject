from django.urls import path
from .views import *


urlpatterns = [
    path('<str:category_id>/<int:article_id>/add_comment/', add_comment, name='add_comment'),
    path('add_article/', add_article, name='add'),
    path('<str:category_id>/', by_category, name='by_category'),
    path('<str:category_id>/<int:article_id>/', by_article, name='by_article'),
    path('', index, name='index'),
]
