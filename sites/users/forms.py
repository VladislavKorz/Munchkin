from django import forms
from django.contrib.auth.forms import UserCreationForm
from loguru import logger

from .models import *
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password1', 'password2']



class EmailConfirmationForm(forms.Form):
    code = forms.CharField(max_length=6, label='Код подтверждения')
