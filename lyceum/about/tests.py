from http import HTTPStatus

from django.test import Client, TestCase


class AboutStaticURLTests(TestCase):
    def test_about_endpoint(self):
        response = Client().get("/about/")
        self.assertEqual(response.status_code, HTTPStatus.OK)


__all__ = [
    AboutStaticURLTests,
]
