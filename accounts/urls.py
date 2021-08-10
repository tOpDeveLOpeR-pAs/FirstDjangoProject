from django.urls import path, include
from .views import *
from djangoProject.settings import LOGIN_REDIRECT_URL

urlpatterns = [
    path('login/', user_login, name="login"),
    path('profile/', user_profile, name="profile"),
    path('', include('django.contrib.auth.urls')),
    path('register/', register, name="register"),
]