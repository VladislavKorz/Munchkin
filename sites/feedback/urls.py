from django.urls import path
from .views import feedback

urlpatterns = [
    path('', feedback, name='feedback'),
    # Добавьте другие URL-паттерны по необходимости
]
