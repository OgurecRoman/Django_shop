import django.core.exceptions
import django.db


def valid_item_text(value):
    if not ("превосходно" in value or "роскошно" in value):
        raise django.core.exceptions.ValidationError(
            "Не найдено слов 'превосходно' или 'роскошно'"
        )


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
    weight = django.db.models.PositiveSmallIntegerField("Вес", default=100)

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
