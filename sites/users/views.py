from django.shortcuts import render
from django.http import HttpResponse
from loguru import logger
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import LoginForm
from .models import *

def LoginViews(request):
    context = {
        "title": "Моя первая страница",
    }
    # Форма логина на сайт
    if not request.user.is_authenticated:
        formLogin = LoginForm(request.POST or None)
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
        return reverse('profile')
    return render(request, 'users/login.html', context)

def ProfileViews(request, username = None):
    if username:
        profile = Profile.objects.filter(user__username = username).first()
    else:
        profile = request.user.profile

    context = {
        "title": f"Манчкин - {profile.user.username}",
        "profile": profile,
    }
    return render(request, 'users/profile.html', context)