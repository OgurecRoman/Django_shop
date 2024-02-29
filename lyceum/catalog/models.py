import django.core.validators
import django.db.models
from django.utils.safestring import mark_safe
from sorl.thumbnail import get_thumbnail
from tinymce.models import HTMLField

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
        default_related_name = "categories"
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
        verbose_name = "тег"
        verbose_name_plural = "теги"
        default_related_name = "tags"

    def __str__(self):
        return self.name


class GalleryImage(django.db.models.Model):
    item = django.db.models.ForeignKey(
        "Item",
        on_delete=django.db.models.CASCADE,
    )

    image = django.db.models.ImageField(
        "изображения",
        upload_to="catalog/",
        null=True,
    )

    class Meta:
        verbose_name = "изображение"
        verbose_name_plural = "изображения"

    def get_image(self):
        return get_thumbnail(
            self.image,
            "300x300",
            crop="center",
            quality=51,
        )


class Item(core.models.PublishedWithNameBaseModel):
    category = django.db.models.ForeignKey(
        Category,
        on_delete=django.db.models.CASCADE,
        verbose_name="категория",
        related_name="items",
        help_text="Выберите категорию",
    )
    tags = django.db.models.ManyToManyField(
        Tag,
        related_name="tags",
    )
    text = HTMLField(
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


class MainImage(django.db.models.Model):
    item = django.db.models.OneToOneField(
        Item,
        on_delete=django.db.models.CASCADE,
        null=True,
    )
    image = django.db.models.ImageField(
        "главное изображение",
        upload_to="catalog/",
        null=True,
    )

    def get_image(self):
        return get_thumbnail(
            self.image,
            "300x300",
            quality=51,
            crop="center",
        )

    def image_thumbnail(self):
        if self.image:
            return mark_safe(f"<img src='{self.image.url}' width='50'>")
        return "Нет изображения"

    image_thumbnail.short_description = "превью"
    image_thumbnail.allow_tags = True

    class Meta:
        default_related_name = "main_image"
        verbose_name = "главное изображение"


__all__ = []
