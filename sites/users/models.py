from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.urls import reverse
from loguru import logger
from datetime import datetime
from django_ckeditor_5.fields import CKEditor5Field

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name="profile")
    photo = models.ImageField("Фото", upload_to="users/profile/photo", blank=True)
    update = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)
    create = models.DateField(verbose_name='Дата создания', auto_now_add=True)

    class Meta:
        ordering = ["create"]
        verbose_name_plural='Профиль пользователей'
        verbose_name='Профиль пользователя'

    def get_absolute_url(self):
        return reverse('user-publicProfile', args=[str(self.user.username)])

    def __str__(self):
        return str(self.user.username)


class RulesBook(models.Model):
    title = models.CharField("Заголовок", max_length=100)
    user = models.ForeignKey(Profile, verbose_name="Владелец книги", on_delete=models.CASCADE)
    update = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)
    create = models.DateField(verbose_name='Дата создания', auto_now_add=True)

    class Meta:
        ordering = ["title"]
        verbose_name_plural='Книга правил'
        verbose_name='Книга правил'


class RulesSingle(models.Model):
    book = models.ForeignKey(RulesBook, verbose_name="Книга", on_delete=models.CASCADE)
    title = models.CharField("Заголовок", max_length=70)
    rules=CKEditor5Field('Правила')
    update = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)
    create = models.DateField(verbose_name='Дата создания', auto_now_add=True)

    class Meta:
        ordering = ["title"]
        verbose_name_plural='Правила из книги'
        verbose_name='Правило из книги'

@receiver(post_save, sender=User)
def new_user(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()