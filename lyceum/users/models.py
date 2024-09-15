import sys

import django.contrib.auth.models
import django.db.models
import django.utils.safestring
import sorl.thumbnail

import users.managers

if "makemigrations" not in sys.argv and "migrate" not in sys.argv:
    def_user = django.contrib.auth.models.User
    def_user._meta.get_field("email")._unique = True


class User(django.contrib.auth.models.User):
    objects = users.managers.UserManager()

    class Meta:
        proxy = True


class Profile(django.db.models.Model):
    def profile_path(self, filename):
        return f"users/{self.user.id}/{filename}"

    user = django.db.models.OneToOneField(
        django.contrib.auth.models.User,
        on_delete=django.db.models.CASCADE,
    )

    birthday = django.db.models.DateField(
        "дата рождения",
        blank=True,
        null=True,
    )

    image = django.db.models.ImageField(
        "аватар",
        upload_to=profile_path,
        null=True,
        blank=True,
    )

    coffee_count = django.db.models.PositiveIntegerField(
        "попытки сварить кофе",
        default=0,
    )

    attempts_count = django.db.models.PositiveIntegerField(
        verbose_name="попыток входа",
        help_text="Количество попыток входа",
        default=0,
    )
    freeze_date = django.db.models.DateTimeField(
        verbose_name="дата заморозки",
        help_text="дата заморозки",
        null=True,
        blank=True,
    )

    def get_image_300x300(self):
        return sorl.thumbnail.get_thumbnail(
            self.image,
            "300x300",
            crop="center",
            quality=51,
        )

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"


__all__ = []
