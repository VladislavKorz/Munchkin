from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', HomeViews, name='home'),
]
