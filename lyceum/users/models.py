from django.contrib.auth.models import User
import django.db.models
import django.utils.safestring
import sorl.thumbnail


class Profile(django.db.models.Model):
    def profile_path(self, filename):
        return f"users/{self.user.id}/{filename}"

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
        upload_to=profile_path,
        null=True,
        blank=True,
    )

    coffee_count = django.db.models.PositiveIntegerField(
        "попытки сварить кофе",
        default=0,
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
