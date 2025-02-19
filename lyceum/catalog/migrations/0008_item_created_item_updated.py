# Generated by Django 4.2 on 2024-03-14 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "catalog",
            "0007_mainimage_image_alter_item_category_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="created",
            field=models.DateTimeField(
                auto_now_add=True,
                null=True,
                verbose_name="время создания",
            ),
        ),
        migrations.AddField(
            model_name="item",
            name="updated",
            field=models.DateTimeField(
                auto_now=True,
                null=True,
                verbose_name="время изменения",
            ),
        ),
    ]
