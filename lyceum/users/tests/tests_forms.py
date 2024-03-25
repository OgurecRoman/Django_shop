import datetime

import django.conf
import django.core.exceptions
import django.test
import django.urls
import django.utils.timezone
import mock
import parameterized

import users.models


class UsersTests(django.test.TestCase):
    def test_with_login(self):
        client = django.test.Client()
        client.login(username="Тестировщик", password="12345ytrewq")
        client.get("/auth/profile/")

    @django.test.override_settings(DEFAULT_USER_IS_ACTIVE=False)
    def test_user_activation_positive(self):
        self.assertFalse(users.models.User.objects.exists())
        self.client.post(
            django.urls.reverse("users:signup"),
            data={
                "username": "test_username",
                "password1": "VeryStr0ngPa$$",
                "password2": "VeryStr0ngPa$$",
            },
        )
        self.assertFalse(users.models.User.objects.first().is_active)
        self.client.get(
            django.urls.reverse("users:activate", args=["test_username"]),
        )
        self.assertTrue(users.models.User.objects.first().is_active)

    @django.test.override_settings(DEFAULT_USER_IS_ACTIVE=False)
    def test_user_activation_negative(self):
        self.assertFalse(users.models.User.objects.exists())
        self.client.post(
            django.urls.reverse("users:signup"),
            data={
                "username": "test_username",
                "password1": "VeryStr0ngPa$$",
                "password2": "VeryStr0ngPa$$",
            },
        )
        self.assertFalse(users.models.User.objects.first().is_active)
        expired_dt = django.utils.timezone.now() + datetime.timedelta(hours=13)
        with mock.patch("django.utils.timezone.now") as mocked_timezone:
            mocked_timezone.return_value = expired_dt
            self.client.get(
                django.urls.reverse("users:activate", args=["test_username"]),
            )

        self.assertFalse(users.models.User.objects.first().is_active)

    def test_user_signup_positive(self):
        self.assertFalse(users.models.User.objects.exists())
        self.client.post(
            django.urls.reverse("users:signup"),
            data={
                "username": "test_username",
                "password1": "VeryStr0ngPa$$",
                "password2": "VeryStr0ngPa$$",
            },
        )
        self.assertTrue(users.models.User.objects.exists())
        self.assertEqual(
            users.models.User.objects.first().username,
            "test_username",
        )

    def test_user_signup_negative(self):
        self.assertFalse(users.models.User.objects.exists())
        self.client.post(
            django.urls.reverse("users:signup"),
            data={
                "username": "test_username",
                "password1": "simple",
                "password2": "simple",
            },
        )
        self.assertFalse(users.models.User.objects.exists())

    @parameterized.expand(
        (
            ("John.Doe+JaneDOE+gmail.gom@ya.ru", "john-doe@yandex.ru"),
            ("John.Doe+JaneDOE+gmail.gom@gmail.com", "johndoe@gmail.com"),
        ),
    )
    @django.test.override_settings(DEFAULT_USER_IS_ACTIVE=True)
    def test_user_signup_normalized_emails(self, bad_mail, good_mail):
        data = {
            "username": "test_username",
            "email": bad_mail,
            "password1": "strong_password",
            "password2": "strong_password",
        }
        self.client.post(
            django.urls.reverse("users:signup"),
            data,
        )

        users.models.User.objects.by_mail(bad_mail)

        self.assertRaises(
            users.models.User.DoesNotExist,
        )

        created_user = users.models.User.objects.by_mail(good_mail)

        self.assertEqual(
            created_user.username,
            data["username"],
        )

    @django.test.override_settings(DEFAULT_USER_IS_ACTIVE=True)
    def test_user_freeze(self):
        data = {
            "username": "test_username",
            "email": "john_doe@ya.ru",
            "password1": "strong_password",
            "password2": "strong_password",
        }
        self.client.post(
            django.urls.reverse("users:signup"),
            data,
        )

        created_user = users.models.User.objects.get(username=data["username"])

        auth_data = {
            "username": data["username"],
            "password": "wrong_password",
        }

        self.assertTrue(created_user.is_active)

        for login_attempt in range(django.conf.settings.MAX_AUTH_ATTEMPTS):
            with self.subTest(login_attempt=login_attempt):
                self.client.post(
                    django.urls.reverse("users:login"),
                    auth_data,
                )

        created_user = users.models.User.objects.get(username=data["username"])

        self.assertFalse(created_user.is_active)

        return auth_data


__all__ = []
