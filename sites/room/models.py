import datetime

from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.crypto import get_random_string
from users.models import CustomUser

ROOMS_CODE_LENGHT = 5

class Rooms(models.Model):
    ROOM_TYPE_CHOICES = (
        ('O', 'Открытая'),
        ('C', 'Одиночная'),
        ('S', 'Закрытая'),
    )
    code = models.CharField("Номер комнаты", max_length=5, unique=True, default=get_random_string(ROOMS_CODE_LENGHT))
    duration = models.TimeField("Продолжительность игры", default=datetime.time(00, 00))
    room_type = models.CharField("Тип игры", max_length = 1, choices = ROOM_TYPE_CHOICES, default='O')
    leavel_to_win = models.IntegerField("Сколько нужно уровней для победы", default=10)
    rules_book = models.ForeignKey("users.RulesBook", verbose_name="Книга правил для комнаты", on_delete=models.SET_NULL, null=True)
    admin = models.ForeignKey("users.CustomUser", verbose_name="Админ комнаты", on_delete=models.SET_NULL, null=True, related_name='roomAdmin')
    owner = models.ForeignKey("users.CustomUser", verbose_name="Владелец комнаты", on_delete=models.SET_NULL, null=True, related_name="roomOwner")
    end = models.BooleanField("Игра завершилась?", default=False)

    update = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)
    create = models.DateTimeField(verbose_name='Дата старта', auto_now_add=True)

    class Meta:
        verbose_name = "Комната"
        verbose_name_plural = "Комнаты"

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return reverse("room", kwargs={"room_code": self.code})


class RoomPlayer(models.Model):
    room = models.ForeignKey("room.Rooms", verbose_name="Комната", on_delete=models.SET_NULL, null=True, related_name='player')
    player = models.ForeignKey("users.CustomUser", verbose_name="Игрок", on_delete=models.SET_NULL, null=True, related_name='roomPlayer')
    order = models.IntegerField("Порядок игроков", default=1)
    gender = models.CharField("Пол", max_length = 1, choices = CustomUser.GENDER_CHOICES, default='O')
    
    update = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)
    create = models.DateTimeField(verbose_name='Дата старта', auto_now_add=True)

    def get_leavel(self):
        return self.leavel.all().order_by('-pk').first().leavel

    def get_power(self):
        return self.power.all().order_by('-pk').first().power
    
    def get_racer(self):
        if self.playerRace.all():
            return self.playerRace.all().order_by('-pk').first().get_value_display()
        else:
            return None
    
    def get_class(self):
        if self.playerClass.all():
            return self.playerClass.all().order_by('-pk').first().get_value_display()
        else:
            return None

    class Meta:
        ordering = ['-order']
        verbose_name = "Игрок комнаты"
        verbose_name_plural = "Игрок комнаты"

    def __str__(self):
        return f"{self.room} - {self.player}"

class PlayerLeavel(models.Model):
    player = models.ForeignKey("room.RoomPlayer", verbose_name="Игрок", on_delete=models.CASCADE, null=True, related_name='leavel')
    leavel = models.IntegerField("Уровень", default=1)
    create = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    class Meta:
        ordering = ['-create']
        verbose_name = "Уровень игроков в игре"


class PlayerPower(models.Model):
    player = models.ForeignKey("room.RoomPlayer", verbose_name="Игрок", on_delete=models.CASCADE, null=True, related_name='power')
    power = models.IntegerField("Мощность", default=0)
    create = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    class Meta:
        ordering = ['-create']
        verbose_name = "Мощность игроков в игре"

class PlayerClass(models.Model):
    CLASS_CHOICES = (
        ('N', 'Нет'),
        ('W', 'Воин'),
        ('M', 'Волшебник'),
        ('T', 'Вор'),
        ('C', 'Клирик'),
    )
    
    player = models.ForeignKey("room.RoomPlayer", verbose_name="Игрок", on_delete=models.CASCADE, null=True, related_name='playerClass')
    value = models.CharField("Класс", max_length = 1, choices = CLASS_CHOICES, default='N')
    create = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    class Meta:
        ordering = ['-pk']


class PlayerRace(models.Model):
    CLASS_CHOICES = (
        ('H', 'Человек'),
        ('W', 'Эльф'),
        ('M', 'Дварф'),
        ('T', 'Хафлингом'),
    )
    player = models.ForeignKey("room.RoomPlayer", verbose_name="Игрок", on_delete=models.CASCADE, null=True, related_name='playerRace')
    value = models.CharField("Класс", max_length = 1, choices = CLASS_CHOICES, default='H')
    create = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    class Meta:
        ordering = ['-pk']

class RoomBattle(models.Model):
    monster = models.IntegerField("Итоговая сила монстра", default=0)
    player = models.IntegerField("Итоговая сила игрока/команды", default=0)
    
    update = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)
    create = models.DateTimeField(verbose_name='Дата старта', auto_now_add=True)

class RoomBattlePlayer(models.Model):
    battle = models.ForeignKey("room.RoomBattle", verbose_name="Битва", on_delete=models.CASCADE, null=True)
    player = models.ForeignKey("room.RoomPlayer", verbose_name="Игрок", on_delete=models.CASCADE, null=True)
    power = models.IntegerField("Усиления игрока", default=0)

    update = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)
    create = models.DateTimeField(verbose_name='Дата старта', auto_now_add=True)

class RoomBattleMonster(models.Model):
    battle = models.ForeignKey("room.RoomBattle", verbose_name="Битва", on_delete=models.CASCADE, null=True)
    leavel = models.IntegerField("Сила монстра", default=2)
    power = models.IntegerField("Усиления монстра", default=0)

    update = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)
    create = models.DateTimeField(verbose_name='Дата старта', auto_now_add=True)



@receiver(pre_save, sender=Rooms)
def get_random_code(sender, instance, *args, **kwargs):
    if instance.code:
        code = instance.code
        room = Rooms.objects.filter(code = code)
        while room.count() != 0:
            code = get_random_string(ROOMS_CODE_LENGHT)
            room = Rooms.objects.filter(code = code)
        instance.code = code
        return code


@receiver(post_save, sender=RoomPlayer)
def add_models(sender, instance, created=False, *args, **kwargs):
    if instance and created:
        PlayerLeavel.objects.create(player=instance)
        PlayerPower.objects.create(player=instance)
        PlayerClass.objects.create(player=instance)
        PlayerRace.objects.create(player=instance)