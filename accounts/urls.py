from django.urls import path, include
from .views import *


urlpatterns = [
    path('login/', user_login, name="login"),
    path('profile/', user_profile, name="profile"),
    path('logout/', UserLogoutView.as_view(), name="logout"),
    path('', include('django.contrib.auth.urls')),
    path('register/', register, name="register"),
    path('add_article/', add_article, name='add'),
    path('<int:article_id>/update', update_article, name="update"),
    path('<int:article_id>/delete', delete_article, name="delete")
]