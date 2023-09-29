from random import randint

import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import (HttpResponse, HttpResponseNotFound,
                         HttpResponseRedirect)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from loguru import logger
from room.models import *
from users.services import *

from .forms import CustomUserCreationForm, EmailConfirmationForm
# from .forms import LoginForm, RegisterForm
from .models import *


class LoginView(View):
    form_class = AuthenticationForm
    template_name = 'users/login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'title': 'Манчкин-Вход'})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request, request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('profile')
        return render(request, self.template_name, {'form': form, 'title': 'Манчкин-Вход'})


@login_required
def ProfileViews(request, email=None):
    if email:
        profile = CustomUser.objects.filter(email=email).first()
    else:
        profile = request.user
    if not profile:
        return HttpResponseNotFound('Пользователь не найден')
    if request.POST:
        if request.POST.get('room'):
            return HttpResponseRedirect(reverse('room', args=(request.POST.get('room'),)))

    context = {
        "title": f"Манчкин - {profile}",
        "games_count": get_games_count(profile),
        "games_won": get_victories(profile),
        "profile": profile,
        "type_room": Rooms.ROOM_TYPE_CHOICES
    }
    return render(request, 'users/profile.html', context)


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Логиним пользователя сразу после регистрации
            login(request, user)
            user.email_confirmation_code = str(randint(100000, 999999))
            user.save()

            subject = 'Код подтверждения'
            url = reverse('confirm_email_link', args=[request.user.id, user.email_confirmation_code])
            message = f'Ваш код подтверждения: {user.email_confirmation_code}\nСсылка для подтверждения: {request.scheme}://{request.get_host()}{url}'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [user.email]

            send_mail(subject, message, from_email, recipient_list)

            return redirect('confirm_email')  # Перенаправляем на страницу профиля
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form, 'title': 'Манчкин-Регистрация'})



@login_required
def confirm_email(request):
    if request.method == 'POST':
        form = EmailConfirmationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            # Реализуйте здесь вашу логику проверки кода и подтверждения почты
            user = request.user
            if user.email_confirmation_code == code:
                user.email_verify = True
                user.save()

                return redirect('profile')  # Замените 'success_page' на вашу страницу успеха
            else:
                messages.error(request, 'Неправильный код подтверждения.')

    else:
        form = EmailConfirmationForm()

    return render(request, 'users/confirm_email.html', {'form': form})



def confirm_email_link(request, user_id, confirmation_code):
    user = get_object_or_404(CustomUser, id=int(user_id))

    if user.email_confirmation_code == confirmation_code:
        user.email_verify = True
        user.save()
        # Опционально: добавьте здесь какую-то логику для случая успешного подтверждения

        return redirect('profile')  # Замените 'success_page' на вашу страницу успеха


def connect_room(request):
    if request.method == 'POST':
        room_code = request.POST.get('room')

        # Получите текущего пользователя (CustomUser)
        user = request.user

        # Найдите комнату по её коду
        room = Rooms.objects.get(code=room_code)

        # Создайте запись в RoomPlayer, связав пользователя с комнатой
        room_player = RoomPlayer(room=room, player=user)
        room_player.save()

        # Верните что-то, что должно отобразиться после успешного подключения к комнате

        return HttpResponseRedirect(reverse('room', args=(room_code,)))



def make_connection_request(request):
    if request.method == 'POST':
        room_code = request.POST.get('room')

        # Получите текущего пользователя (CustomUser)
        user = request.user

        # Найдите комнату по её коду
        room = Rooms.objects.get(code=room_code)

        # Создайте запись в RoomPlayer, связав пользователя с комнатой
        room_player = ConnectionRequest(room=room, player=user)
        room_player.save()

        # Верните что-то, что должно отобразиться после успешного подключения к комнате

        return redirect('profile')


def make_qr_connection_request(request, code):
    if request.method == 'GET':

        # Получите текущего пользователя (CustomUser)
        user = request.user

        # Найдите комнату по её коду
        room = Rooms.objects.get(code=code)

        # Создайте запись в RoomPlayer, связав пользователя с комнатой
        room_player = ConnectionRequest(room=room, player=user)
        room_player.save()

        # Верните что-то, что должно отобразиться после успешного подключения к комнате

        return redirect('profile')
