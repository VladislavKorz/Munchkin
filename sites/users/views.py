import requests
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import (HttpResponse, HttpResponseNotFound,
                         HttpResponseRedirect)
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from loguru import logger
from room.models import *

from .forms import CustomUserCreationForm
# from .forms import LoginForm, RegisterForm
from .models import *


class LoginView(View):
    form_class = AuthenticationForm
    template_name = 'users/login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

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
        return render(request, self.template_name, {'form': form})


@login_required
def ProfileViews(request, username=None):
    if username:
        profile = CustomUser.objects.filter().first()
    else:
        profile = request.user
    if not profile:
        return HttpResponseNotFound('Пользователь не найден')
    if request.POST:
        if request.POST.get('room'):
            return HttpResponseRedirect(reverse('room', args=(request.POST.get('room'),)))

    context = {
        "title": f"Манчкин - {profile}",
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
            return redirect('profile')  # Перенаправляем на страницу профиля
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})
