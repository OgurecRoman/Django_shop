from django.contrib.auth.models import User
import django.db.models


def profile_directory_path(instance, filename):
    return f"users/{instance.user.id}/{filename}"


class Profile(django.db.models.Model):
    user = django.db.models.OneToOneField(
        User,
        on_delete=django.db.models.CASCADE,
    )

    birthday = django.db.models.DateField(
        "дата рождения",
        null=True,
        blank=True,
    )

    image = django.db.models.ImageField(
        "аватар",
        upload_to=profile_directory_path,
        blank=True,
    )

    coffee_count = django.db.models.PositiveIntegerField(
        "попытки сварить кофе",
        default=0,
    )

    class Meta:
        verbose_name = "дополнительное поле"
        verbose_name_plural = "дополнительные поля"


__all__ = []
