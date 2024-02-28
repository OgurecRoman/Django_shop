import django.core.validators
import django.db.models

import catalog.validators
import core.models


class Category(core.models.PublishedWithNameBaseModel):
    slug = django.db.models.SlugField(
        "слаг",
        max_length=200,
        help_text="Максимум 200 символов",
    )
    weight = django.db.models.PositiveSmallIntegerField(
        "вес",
        validators=[
            django.core.validators.MinValueValidator(
                1,
                message="Значение должно быть больше 0",
            ),
            django.core.validators.MaxValueValidator(
                32767,
                message="Значение должно быть меньше 32767",
            ),
        ],
        default=100,
        help_text="Max 32767",
    )

    class Meta:
        ordering = ("weight", "id")
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return self.name


class Tag(core.models.PublishedWithNameBaseModel):
    slug = django.db.models.SlugField(
        "слаг",
        max_length=200,
        unique=True,
    )

    class Meta:
        ordering = ("slug",)
        verbose_name = "тег"
        verbose_name_plural = "теги"
        default_related_name = "tags"

    def __str__(self):
        return self.name


class Item(core.models.PublishedWithNameBaseModel):
    category = django.db.models.ForeignKey(
        Category,
        on_delete=django.db.models.CASCADE,
        verbose_name="категория",
        help_text="Выберите категорию",
    )
    tags = django.db.models.ManyToManyField(
        Tag,
    )
    text = django.db.models.TextField(
        "описание",
        validators=[
            catalog.validators.WordsValidator(
                "превосходно",
                "роскошно",
            ),
        ],
        help_text="Введите описание объекта",
    )

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"
        default_related_name = "items"

    def __str__(self):
        return self.name
