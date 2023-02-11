from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('login/', LoginViews, name='login'),
    path('<str:username>/', ProfileViews, name='profile'),
    path('', ProfileViews, name='profile'),
    # path('', LogoutViews, name='logout'),
]
