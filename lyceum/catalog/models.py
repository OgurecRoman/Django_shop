import re

import django.core.exceptions
import django.db


def valid_item_text(value):
    words = re.compile(r"\w+|\W+").findall(value)
    words = map(str.lower, words)
    if not ("превосходно" in words or "роскошно" in words):
        raise django.core.exceptions.ValidationError(
            "Не найдено слов 'превосходно' или 'роскошно'"
        )


def valid_category_weight(value):
    if not (int(value) in range(1, 32768)):
        raise django.core.exceptions.ValidationError("От 0 до 32767")


class AbstructModel(django.db.models.Model):
    name = django.db.models.CharField("Название", max_length=150)
    is_published = django.db.models.BooleanField("Опубликовано", default=True)

    class Meta:
        abstract = True


class Tag(AbstructModel):
    slug = django.db.models.SlugField("Слаг", max_length=200, unique=True)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class Category(AbstructModel):
    slug = django.db.models.SlugField("Слаг", max_length=200, unique=True)
    weight = django.db.models.SmallIntegerField(
        "Вес", default=100, validators=[valid_category_weight]
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Item(AbstructModel):
    text = django.db.models.TextField(
        "Текст",
        help_text="Введите описание объекта",
        validators=[valid_item_text],
    )
    category = django.db.models.ForeignKey(
        "category",
        on_delete=django.db.models.CASCADE,
        related_name="catalog_item",
        verbose_name="Категория",
    )
    tags = django.db.models.ManyToManyField(Tag, verbose_name="Теги")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
