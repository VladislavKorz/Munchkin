from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path

from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', register, name='users_register'),

    path('logout/', LogoutView.as_view(), name='logout'),
    path('<str:username>/', ProfileViews, name='profile'),
    path('', ProfileViews, name='profile'),
    # path('', LogoutViews, name='logout'),
]
