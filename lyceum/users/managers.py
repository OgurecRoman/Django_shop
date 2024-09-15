import django.contrib.auth.models
import django.db.models
import django.utils.safestring


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
