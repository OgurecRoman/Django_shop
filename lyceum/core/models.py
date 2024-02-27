import re

import django.db.models

ONLY_LETTERS_REGEX = re.compile(r"[^\w]")


class PublishedWithNameBaseModel(django.db.models.Model):
    name = django.db.models.CharField(
        "название",
        max_length=150,
        unique=True,
        help_text="Максимум 150 символов",
    )
    is_published = django.db.models.BooleanField("опубликовано", default=True)

    class Meta:
        abstract = True
