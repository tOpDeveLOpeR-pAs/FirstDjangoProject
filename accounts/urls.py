from django.urls import path, include
from .views import *
from django.contrib.auth.views import PasswordChangeView


urlpatterns = [
    path('login/', user_login, name="login"),
    path('profile/', user_profile, name="profile"),
    path('logout/', UserLogoutView.as_view(), name="logout"),
    path('change_password/', UserPasswordChangeView.as_view(), name="change_password"),
    path('', include('django.contrib.auth.urls')),
    path('register/', register, name="register"),
    path('add_article/', add_article, name='add'),
    path('<int:article_id>/update', update_article, name="update"),
    path('<int:article_id>/delete', delete_article, name="delete")
]