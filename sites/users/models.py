from datetime import datetime

from django.contrib.auth.models import (AbstractBaseUser, AbstractUser,
                                        BaseUserManager, PermissionsMixin,
                                        User)
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field
from loguru import logger

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Мужской'),
        ('F', 'Женский'),
        ('O', 'Не задано'),
    )


    LANGUAGE_CHOICES = (
        ('ru', 'Русский'),
        ('en', 'Английский'),
        ('de', 'Немецкий'),
        ('ch', 'Китайский'),
    )


    username = models.CharField('username', max_length=30, unique=True)
    email = models.EmailField('email address', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = CustomUserManager()

    name = models.CharField('имя пользователя', max_length=64, blank=True, null=True)
    email_verify = models.BooleanField(default=False)
    email_confirmation_code = models.CharField(max_length=6, blank=True, null=True)
    language = models.CharField("Язык", max_length=2, choices=LANGUAGE_CHOICES, default='ru')
    photo = models.ImageField(
        "Фото", upload_to="users/profile/photo", blank=True)
    gender = models.CharField(
        "Пол", max_length=1, choices=GENDER_CHOICES, default='O')
    update = models.DateTimeField(
        verbose_name='Дата обновления', auto_now=True)
    create = models.DateField(verbose_name='Дата создания', auto_now_add=True)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ["create"]
        verbose_name_plural = 'Профиль пользователей'
        verbose_name = 'Профиль пользователя'

    def get_all_activities(self):
        def create_elem(room_obj, actions):
            elem = {
                'datetime': room_obj.create,
                'title': actions,
                'code': room_obj.code,
                'room_url': room_obj.get_absolute_url(),
                'game_end': room_obj.end,
                'winner': False,
                'players': [{
                    'username': player.player.username,
                    'url': player.player.get_absolute_url(),
                    'photo': player.player.get_photo_url(),
                } for player in room_obj.player.all()]
            }
            return elem

        activities_list = []
        for item in self.roomOwner.all():
            if item:
                activities_list.append(create_elem(item, 'Начал игру'))
        for item in self.roomPlayer.all():
            if item.room:
                if item.room.code not in [i['code'] for i in activities_list]:
                    activities_list.append(create_elem(
                        item.room, 'Участвовал в игре'))
        activities_list_sort = sorted(
            activities_list, key=lambda d: d['datetime'], reverse=True)

        return activities_list_sort

    def get_absolute_url(self):
        return reverse('profile', args=[str(self.email)])

    def get_photo_url(self):
        if self.photo:
            return self.photo.url
        else:
            return 'https://bootdey.com/img/Content/avatar/avatar7.png'

    def __str__(self):
        return str(self.email)


class RulesBook(models.Model):
    title = models.CharField("Заголовок", max_length=100)
    user = models.ForeignKey(CustomUser, verbose_name="Владелец книги",
                             on_delete=models.CASCADE, related_name='rulesBook')
    update = models.DateTimeField(
        verbose_name='Дата обновления', auto_now=True)
    create = models.DateField(verbose_name='Дата создания', auto_now_add=True)

    class Meta:
        ordering = ["title"]
        verbose_name_plural = 'Книга правил'
        verbose_name = 'Книга правил'


class RulesSingle(models.Model):
    book = models.ForeignKey(
        RulesBook, verbose_name="Книга", on_delete=models.CASCADE)
    title = models.CharField("Заголовок", max_length=70)
    rules = CKEditor5Field('Правила')
    update = models.DateTimeField(
        verbose_name='Дата обновления', auto_now=True)
    create = models.DateField(verbose_name='Дата создания', auto_now_add=True)

    class Meta:
        ordering = ["title"]
        verbose_name_plural = 'Правила из книги'
        verbose_name = 'Правило из книги'
