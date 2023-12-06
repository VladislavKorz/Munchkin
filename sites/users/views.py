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
from django.views.generic import ListView
from .models import CustomUser
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
import random
import string
from django.contrib.auth.views import LogoutView

from .forms import CustomUserCreationForm, EmailConfirmationForm
# from .forms import LoginForm, RegisterForm
from .models import *
from .tasks import send_email_verification


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

            send_email_verification.delay(subject, message, from_email, recipient_list)

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


def connect_room(request, room):
    if request.method == 'GET':
    # if request.method == 'POST':
        # room_code = request.POST.get('room')

        # Получите текущего пользователя (CustomUser)
        user = request.user
        room = Rooms.objects.get(code=room)

        if not user.is_authenticated:
            return redirect('login')

        if connection:=ConnectionRequest.objects.filter(player=user, room=room).last():
            if connection.approved !=True:
                return redirect('profile')

            else:
                if not connection.spectator:
                    # Создайте запись в RoomPlayer, связав пользователя с комнатой
                    room_player = RoomPlayer(room=room, player=user)
                    room_player.save()

                # Верните что-то, что должно отобразиться после успешного подключения к комнате

                return HttpResponseRedirect(reverse('room', args=(room,)))

        return redirect('profile')


def make_connection_request(request):
    if request.method == 'POST':
        try:
            room_code = request.POST.get('room')

            # Получите текущего пользователя (CustomUser)
            user = request.user

            # Найдите комнату по её коду
            room = Rooms.objects.get(code=room_code)

            my_checkbox = request.POST.get('my_checkbox')

            # Преобразуйте значение чекбокса в тип bool
            my_checkbox = my_checkbox == 'on'

            if room.owner==request.user or room.admin==request.user:
                return HttpResponseRedirect(reverse('room', args=(room,)))

            elif room.room_type == 'C':
                return render(request, 'room/solo_room_error.html')

            elif any([i.approved==True for i in request.user.connectionPlayer.all()]):
                return HttpResponseRedirect(reverse('room', args=(room,)))

            else:
                # Создайте запись в RoomPlayer, связав пользователя с комнатой
                if my_checkbox:
                    room_player = ConnectionRequest(room=room, player=user, spectator=True)
                    room_player.save()
                else:
                    room_player = ConnectionRequest(room=room, player=user)
                    room_player.save()

                # Верните что-то, что должно отобразиться после успешного подключения к комнате

                # context = {'room_code': room_code, 'user': user, 'connection': room_player}
                # return render(request, 'users/wait_to_connect.html', context)

                url = reverse('wait_to_connect', args=(room_player.id,))

                # Перенаправьте пользователя на новую страницу
                return HttpResponseRedirect(url)

        except Rooms.DoesNotExist:
                # Обработка ситуации, когда комната с указанным кодом не найдена
                # Верните сообщение об ошибке или выполните другие действия по вашему усмотрению
                return HttpResponse("Код комнаты не может быть пустым.")


def wait_to_connect(request, connection_id):

    # Найдите связанную запись ConnectionRequest
    connection = ConnectionRequest.objects.get(pk=connection_id)
    room = Rooms.objects.get(code=connection.room.code)

    # Верните что-то, что должно отобразиться на странице ожидания подключения
    context = {'room': room, 'user': connection.player, 'connection': connection}
    return render(request, 'users/wait_to_connect.html', context)



def make_qr_connection_request(request, code):
    if request.method == 'GET':

        # Получите текущего пользователя (CustomUser)
        user = request.user


        # Найдите комнату по её коду
        room = Rooms.objects.get(code=code)

        # Создайте запись в RoomPlayer, связав пользователя с комнатой
        room_player = ConnectionRequest(room=room, player=user)
        room_player.save()


        url = reverse('wait_to_connect', args=(room_player.id,))

        # Перенаправьте пользователя на новую страницу
        return HttpResponseRedirect(url)






# Ваше приложение/views.py
def create_guest(request):
    User = get_user_model()

    # Генерируем рандомную почту и пароль
    random_email = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '@guest.com'
    random_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    random_username = 'guest-' + ''.join(random.choices(string.ascii_letters + string.digits, k=9))

    # Создаем пользователя
    user = User.objects.create_user(username=random_username, email=random_email, password=random_password, email_verify=True, guest=True)
    login(request, user)

    # Редиректим на страницу успешного создания пользователя или куда вам нужно
    return redirect('profile')  # Замените 'success_page' на ваш URL-путь для страницы успеха



class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        response = super().dispatch(request, *args, **kwargs)

        # Проверяем, является ли пользователь гостем (если это поле guest у юзера True)
        if user.is_authenticated and hasattr(user, 'guest') and user.guest:
            User = get_user_model()
            # Дополнительные действия перед удалением пользователя, если необходимо
            # ...

            # Удаляем пользователя
            user.delete()

        return response