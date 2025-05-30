from http import HTTPStatus

from django.test import Client, TestCase
import django.urls


class AboutStaticURLTests(TestCase):
    def test_about_endpoint(self):
        response = Client().get(django.urls.reverse("about:about"))
        self.assertEqual(response.status_code, HTTPStatus.OK)


__all__ = []
