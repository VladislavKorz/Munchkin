from django import forms
from .models import *
from loguru import logger
from snowpenguin.django.recaptcha3.fields import ReCaptchaField

class LoginForm(forms.Form):
    email = forms.CharField(label="email", widget=forms.EmailInput(
        attrs={'placeholder':'Email','id': 'inputlogin', 'class': 'form-control'}))
    password = forms.CharField( widget=forms.PasswordInput(
        attrs={'placeholder':'Пароль', 'id': 'inputPassword', 'class': 'form-control'}))
    captcha = ReCaptchaField(score_threshold=0.5)
