# Generated by Django 4.1.6 on 2023-02-15 08:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='roombattle',
            name='create',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата старта'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='roombattle',
            name='update',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата обновления'),
        ),
        migrations.AddField(
            model_name='roombattlemonster',
            name='create',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата старта'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='roombattlemonster',
            name='update',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата обновления'),
        ),
        migrations.AddField(
            model_name='roombattleplayer',
            name='create',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата старта'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='roombattleplayer',
            name='update',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата обновления'),
        ),
        migrations.AddField(
            model_name='roomplayer',
            name='gender',
            field=models.CharField(choices=[('M', 'Мужской'), ('F', 'Женский'), ('O', 'Не задано')], default='O', max_length=1, verbose_name='Пол'),
        ),
        migrations.AlterField(
            model_name='rooms',
            name='code',
            field=models.CharField(default='YxFVx', max_length=5, unique=True, verbose_name='Номер комнаты'),
        ),
    ]
