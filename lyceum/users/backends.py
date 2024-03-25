import django.conf
import django.contrib.auth.backends
import django.core.mail
import django.urls
import django.utils
import django.utils.timezone

import users.models

__all__ = []


class LoginBackend(django.contrib.auth.backends.ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            if "@" in username:
                user = users.models.User.objects.by_mail(username)
            else:
                user = users.models.User.objects.get(username=username)

            if user.check_password(password):
                user.profile.attempts_count = 0
                user.profile.save()
                return user

            user.profile.attempts_count += 1
            if (
                user.profile.attempts_count
                >= django.conf.settings.MAX_AUTH_ATTEMPTS
            ):
                user.is_active = False
                user.profile.freeze_date = django.utils.timezone.now()
                user.save()
                activate_url = django.urls.reverse(
                    "users:reactivate",
                    kwargs={"pk": user.id},
                )
                django.core.mail.send_mail(
                    "Блокировка аккаунта",
                    f"Мы заметили подозрительную активность, "
                    f"поэтому ваш аккаунт был заблокирован.\n"
                    f"Перейдите по ссылке для разблокировки ("
                    f"действительна неделю): {activate_url}",
                    django.conf.settings.DJANGO_MAIL,
                    recipient_list=[
                        user.email,
                    ],
                )

            user.profile.save()

            return None

        except users.models.User.DoesNotExist:
            return None
