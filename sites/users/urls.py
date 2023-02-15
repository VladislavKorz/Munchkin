from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [
    path('login/', LoginViews, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('<str:username>/', ProfileViews, name='profile'),
    path('', ProfileViews, name='profile'),
    # path('', LogoutViews, name='logout'),
]
