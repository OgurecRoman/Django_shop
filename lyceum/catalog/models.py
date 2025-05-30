import django.core.validators
import django.db.models
import django.utils.safestring
import sorl.thumbnail
from tinymce.models import HTMLField

import catalog.managers
import catalog.validators
import core.models


def item_directory_path(instance, filename):
    return f"catalog/{instance.item.id}/{filename}"


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
        help_text="Максимальное значение - 32767",
    )

    class Meta:
        ordering = (
            "weight",
            "id",
        )
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
    objects = catalog.managers.Itemmanager()

    category = django.db.models.ForeignKey(
        Category,
        on_delete=django.db.models.CASCADE,
        verbose_name="категория",
        help_text="Выберите категорию",
    )
    tags = django.db.models.ManyToManyField(Tag)

    text = HTMLField(
        "описание",
        validators=[
            catalog.validators.WordsValidator(
                "превосходно",
                "роскошно",
            ),
        ],
        help_text="Описание должно содержать слова "
        "'превосходно' или 'роскошно'.",
    )

    is_on_main = django.db.models.BooleanField(default="False")

    created = django.db.models.DateTimeField(
        "время создания",
        auto_now_add=True,
        null=True,
    )

    updated = django.db.models.DateTimeField(
        "время изменения",
        auto_now=True,
        null=True,
    )

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"
        default_related_name = "items"

    def __str__(self):
        return self.text[:95] + "..."

    def image_tmb(self):
        if self.main_image.image:
            return django.utils.safestring.mark_safe(
                f"<img src='{self.main_image.get_image_50x50.url}'>",
            )

        return "Нет изображения"

    image_tmb.short_description = "превью"
    image_tmb.allow_tags = True


class ImageBaseModel(django.db.models.Model):
    image = django.db.models.ImageField(
        "изображение",
        upload_to=item_directory_path,
        default=None,
    )

    def get_image_300x300(self):
        return sorl.thumbnail.get_thumbnail(
            self.image,
            "300x300",
            crop="center",
            quality=51,
        )

    @property
    def get_image_50x50(self):
        return sorl.thumbnail.get_thumbnail(
            self.image,
            "50x50",
            crop="center",
            quality=51,
        )

    class Meta:
        abstract = True

    def __str__(self):
        return self.item.name


class MainImage(ImageBaseModel):
    item = django.db.models.OneToOneField(
        Item,
        on_delete=django.db.models.CASCADE,
        related_name="main_image",
        help_text="Главное изображение товара "
        "(будет отображаться в списке товаров)",
    )

    class Meta:
        verbose_name = "главное изображение"
        verbose_name_plural = "главные изображения"

    def __str__(self):
        return self.item.name


class Image(ImageBaseModel):
    item = django.db.models.ForeignKey(
        Item,
        on_delete=django.db.models.CASCADE,
        related_name="images",
        help_text="Добавьте больше фотографий, относящихся к товару",
    )

    class Meta:
        verbose_name = "фото"
        verbose_name_plural = "фото"


__all__ = []
