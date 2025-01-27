# Generated by Django 4.1.6 on 2023-09-22 18:25

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MetaTag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("html_path", models.CharField(max_length=64)),
                ("description", models.TextField()),
                ("keywords", models.TextField()),
                ("title", models.CharField(max_length=64)),
            ],
        ),
    ]
