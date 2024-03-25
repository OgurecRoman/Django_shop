import sys

import django.contrib.auth.models
import django.db.models
import django.utils.safestring
import sorl.thumbnail

if "makemigrations" not in sys.argv and "migrate" not in sys.argv:
    def_user = django.contrib.auth.models.User
    def_user._meta.get_field("email")._unique = True


class UserManager(django.contrib.auth.models.UserManager):
    CANONICAL_DOMAINS = {
        "ya.ru": "yandex.ru",
    }
    DOTS = {
        "gmail.com": "",
        "yandex.ru": "-",
    }

    def get_queryset(self):
        user = django.contrib.auth.models.User
        profile = user.profile.related.name
        select = super().get_queryset()
        return select.select_related(profile)

    def by_mail(self, mail):
        normalized_email = self.normalized_email(mail)
        return self.active().get(email=normalized_email)

    def active(self):
        return self.get_queryset().filter(is_active=True)

    @classmethod
    def normalize_email(cls, email):
        email = super().normalize_email(email).lower()

        try:
            email_name, domain_part = email.strip().rsplit("@", 1)
            email_name, *submail = email_name.split("+", 1)

            canonical_domain = cls.CANONICAL_DOMAINS.get(
                domain_part,
                domain_part,
            )

            email_name = email_name.replace(
                ".",
                cls.DOTS.get(
                    canonical_domain,
                    ".",
                ),
            )

        except ValueError:
            pass

        else:
            email = email_name + "@" + canonical_domain.lower()

        return email


class User(django.contrib.auth.models.User):
    objects = UserManager()

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
