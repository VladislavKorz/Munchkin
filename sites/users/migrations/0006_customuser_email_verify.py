# Generated by Django 4.1.6 on 2023-09-21 16:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0005_alter_customuser_username"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="email_verify",
            field=models.BooleanField(default=False),
        ),
    ]
