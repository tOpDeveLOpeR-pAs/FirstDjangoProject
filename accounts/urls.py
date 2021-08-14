from django.urls import path, include
from .views import *


urlpatterns = [
    path('login/', user_login, name="login"),
    path('profile/', user_profile, name="profile"),
    path('', include('django.contrib.auth.urls')),
    path('register/', register, name="register"),
    path('add_article/', ArticleCreateView.as_view(), name='add'),
]