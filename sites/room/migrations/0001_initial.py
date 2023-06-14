# Generated by Django 4.1.6 on 2023-03-27 09:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(choices=[('N', 'Нет'), ('W', 'Воин'), ('M', 'Волшебник'), ('T', 'Вор'), ('C', 'Клирик')], default='N', max_length=1, verbose_name='Класс')),
                ('create', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'ordering': ['-pk'],
            },
        ),
        migrations.CreateModel(
            name='PlayerLeavel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leavel', models.IntegerField(default=1, verbose_name='Уровень')),
                ('create', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Уровень игроков в игре',
                'ordering': ['-create'],
            },
        ),
        migrations.CreateModel(
            name='PlayerPower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('power', models.IntegerField(default=0, verbose_name='Мощность')),
                ('create', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Мощность игроков в игре',
                'ordering': ['-create'],
            },
        ),
        migrations.CreateModel(
            name='PlayerRace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(choices=[('H', 'Человек'), ('W', 'Эльф'), ('M', 'Дварф'), ('T', 'Хафлингом')], default='H', max_length=1, verbose_name='Класс')),
                ('create', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'ordering': ['-pk'],
            },
        ),
        migrations.CreateModel(
            name='RoomBattle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monster', models.IntegerField(default=0, verbose_name='Итоговая сила монстра')),
                ('player', models.IntegerField(default=0, verbose_name='Итоговая сила игрока/команды')),
                ('update', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('create', models.DateTimeField(auto_now_add=True, verbose_name='Дата старта')),
            ],
        ),
        migrations.CreateModel(
            name='RoomBattleMonster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leavel', models.IntegerField(default=2, verbose_name='Сила монстра')),
                ('power', models.IntegerField(default=0, verbose_name='Усиления монстра')),
                ('update', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('create', models.DateTimeField(auto_now_add=True, verbose_name='Дата старта')),
            ],
        ),
        migrations.CreateModel(
            name='RoomBattlePlayer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('power', models.IntegerField(default=0, verbose_name='Усиления игрока')),
                ('update', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('create', models.DateTimeField(auto_now_add=True, verbose_name='Дата старта')),
            ],
        ),
        migrations.CreateModel(
            name='RoomPlayer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=1, verbose_name='Порядок игроков')),
                ('gender', models.CharField(choices=[('M', 'Мужской'), ('F', 'Женский'), ('O', 'Не задано')], default='O', max_length=1, verbose_name='Пол')),
                ('update', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('create', models.DateTimeField(auto_now_add=True, verbose_name='Дата старта')),
            ],
            options={
                'verbose_name': 'Игрок комнаты',
                'verbose_name_plural': 'Игрок комнаты',
                'ordering': ['-order'],
            },
        ),
        migrations.CreateModel(
            name='Rooms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default='bv4EB', max_length=5, unique=True, verbose_name='Номер комнаты')),
                ('duration', models.TimeField(default=datetime.time(0, 0), verbose_name='Продолжительность игры')),
                ('room_type', models.CharField(choices=[('O', 'Открытая'), ('C', 'Одиночная'), ('S', 'Закрытая')], default='O', max_length=1, verbose_name='Тип игры')),
                ('leavel_to_win', models.IntegerField(default=10, verbose_name='Сколько нужно уровней для победы')),
                ('end', models.BooleanField(default=False, verbose_name='Игра завершилась?')),
                ('update', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('create', models.DateTimeField(auto_now_add=True, verbose_name='Дата старта')),
            ],
            options={
                'verbose_name': 'Комната',
                'verbose_name_plural': 'Комнаты',
            },
        ),
    ]