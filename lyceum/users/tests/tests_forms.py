import datetime

import django.core.exceptions
import django.test
import django.urls
import django.utils.timezone
import mock

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


__all__ = []
