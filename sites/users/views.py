from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from loguru import logger
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import LoginForm
from room.models import *
from .models import *
from django.conf import settings
from loguru import logger
import requests

def LoginViews(request):
    context = {
        "title": "Моя первая страница",
        "recaptcha_site_key": settings.RECAPTCHA_PRIVATE_KEY
    }
    # Форма логина на сайт
    if not request.user.is_authenticated:
        formLogin = LoginForm(request.POST or None)
        logger.debug(request.POST)
        if formLogin.is_valid():
            passwordvalue = formLogin.cleaned_data.get("password")
            username = User.objects.filter(email = formLogin.cleaned_data.get("email")).first().username
            user = authenticate(username=username, password=passwordvalue)
            if user is not None:
                login(request, user)
            else:
                context.update(
                    {'Loginform': formLogin, 'errorUserLogin': 'Неправильная комбинация имени пользователя и пароля'})
        else:
            context.update({'Loginform': formLogin})
    else:
        return HttpResponseRedirect(reverse('profile'))
    return render(request, 'users/login.html', context)

@login_required
def ProfileViews(request, username = None):
    if username:
        profile = Profile.objects.filter(user__username = username).first()
    else:
        profile = request.user.profile
    if not profile:
        return HttpResponse('Пользователь не найден')
    if request.POST:
        if request.POST.get('room'):
            return HttpResponseRedirect(reverse('room', args=(request.POST.get('room'),)))

    context = {
        "title": f"Манчкин - {profile.user.username}",
        "profile": profile,
        "type_room": Rooms.ROOM_TYPE_CHOICES
    }
    return render(request, 'users/profile.html', context)