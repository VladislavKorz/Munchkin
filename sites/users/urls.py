from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path
from django.views.generic import TemplateView

from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', register, name='users_register'),
    path('confirm_email/', confirm_email, name='confirm_email'),
    path('confirm_email_link/<str:user_id>/<str:confirmation_code>/',confirm_email_link, name='confirm_email_link'),

    path('logout/', LogoutView.as_view(), name='logout'),
    path('<str:email>/', ProfileViews, name='profile'),
    path('', ProfileViews, name='profile'),
    # path('', LogoutViews, name='logout'),
]
