# Generated by Django 4.1.6 on 2023-09-14 06:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("room", "0005_alter_rooms_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="rooms",
            name="code",
            field=models.CharField(
                default="x3KAt", max_length=5, unique=True, verbose_name="Номер комнаты"
            ),
        ),
    ]
