from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.utils.crypto import get_random_string
from users.models import Profile
import datetime

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
    admin = models.ForeignKey("users.Profile", verbose_name="Админ комнаты", on_delete=models.SET_NULL, null=True, related_name='roomAdmin')
    owner = models.ForeignKey("users.Profile", verbose_name="Владелец комнаты", on_delete=models.SET_NULL, null=True, related_name="roomOwner")
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
    player = models.ForeignKey("users.Profile", verbose_name="Игрок", on_delete=models.SET_NULL, null=True, related_name='roomPlayer')
    order = models.IntegerField("Порядок игроков", default=1)
    gender = models.CharField("Пол", max_length = 1, choices = Profile.GENDER_CHOICES, default='O')
    
    update = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)
    create = models.DateField(verbose_name='Дата старта', auto_now_add=True)

    class Meta:
        ordering = ['-order']
        verbose_name = "Игрок комнаты"
        verbose_name_plural = "Игрок комнаты"

    def __str__(self):
        return str(self.room) + str(self.player)

class PlayerLeavel(models.Model):
    player = models.ForeignKey("room.RoomPlayer", verbose_name="Игрок", on_delete=models.SET_NULL, null=True)
    leavel = models.IntegerField("Уровень", default=1)
    create = models.DateField(verbose_name='Дата создания', auto_now_add=True)


class PlayerPower(models.Model):
    player = models.ForeignKey("room.RoomPlayer", verbose_name="Игрок", on_delete=models.SET_NULL, null=True)
    power = models.IntegerField("Мощность", default=0)
    create = models.DateField(verbose_name='Дата создания', auto_now_add=True)

class PlayerClass(models.Model):
    CLASS_CHOICES = (
        ('W', 'Воин'),
        ('M', 'Волшебник'),
        ('T', 'Вор'),
        ('C', 'Клирик'),
    )
    
    player = models.ForeignKey("room.RoomPlayer", verbose_name="Игрок", on_delete=models.CASCADE, null=True, related_name='playerClass')
    value = models.CharField("Класс", max_length = 1, choices = CLASS_CHOICES, default='O')
    create = models.DateField(verbose_name='Дата создания', auto_now_add=True)
    class Meta:
        ordering = ['-create']


class PlayerRace(models.Model):
    CLASS_CHOICES = (
        ('W', 'Эльф'),
        ('M', 'Дварф'),
        ('T', 'Хафлингом'),
    )
    player = models.ForeignKey("room.RoomPlayer", verbose_name="Игрок", on_delete=models.CASCADE, null=True, related_name='playerRace')
    value = models.CharField("Класс", max_length = 1, choices = CLASS_CHOICES, default='O')
    create = models.DateField(verbose_name='Дата создания', auto_now_add=True)
    class Meta:
        ordering = ['-create']

class RoomBattle(models.Model):
    monster = models.IntegerField("Итоговая сила монстра", default=0)
    player = models.IntegerField("Итоговая сила игрока/команды", default=0)
    
    update = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)
    create = models.DateField(verbose_name='Дата старта', auto_now_add=True)

class RoomBattlePlayer(models.Model):
    battle = models.ForeignKey("room.RoomBattle", verbose_name="Битва", on_delete=models.CASCADE, null=True)
    player = models.ForeignKey("room.RoomPlayer", verbose_name="Игрок", on_delete=models.CASCADE, null=True)
    power = models.IntegerField("Усиления игрока", default=0)

    update = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)
    create = models.DateField(verbose_name='Дата старта', auto_now_add=True)

class RoomBattleMonster(models.Model):
    battle = models.ForeignKey("room.RoomBattle", verbose_name="Битва", on_delete=models.CASCADE, null=True)
    leavel = models.IntegerField("Сила монстра", default=2)
    power = models.IntegerField("Усиления монстра", default=0)

    update = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)
    create = models.DateField(verbose_name='Дата старта', auto_now_add=True)



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