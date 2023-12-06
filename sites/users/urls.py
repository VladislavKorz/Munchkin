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

    path('create_guest/', create_guest, name='create_guest'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('make_connection_request', make_connection_request, name='make_connection_request'),
    path('make_qr_connection_request/<str:code>', make_qr_connection_request, name='make_qr_connection_request'), 
    path('<str:email>/', ProfileViews, name='profile'),
    path('', ProfileViews, name='profile'),
    path('wait_to_connect/<int:connection_id>/', wait_to_connect, name='wait_to_connect'),
    path('connect_room/<str:room>/', connect_room, name='connect_room'),
    # path('', LogoutViews, name='logout'),
]
