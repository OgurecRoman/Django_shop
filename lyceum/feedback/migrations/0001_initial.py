# Generated by Django 4.2 on 2024-03-20 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="FeedbackModel",
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
                ("text", models.TextField(verbose_name="текст")),
                (
                    "created_on",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="время создания"
                    ),
                ),
                (
                    "mail",
                    models.EmailField(max_length=254, verbose_name="почта"),
                ),
            ],
        ),
    ]
