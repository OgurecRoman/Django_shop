from http import HTTPStatus

from django.test import Client, TestCase


class HomepageStaticURLTests(TestCase):
    def test_homepage_endpoint(self):
        response = Client().get("/")
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_coffee_endpoint(self):
        response = Client().get("/coffee/")
        self.assertEqual(response.status_code, HTTPStatus.IM_A_TEAPOT)

    def test_coffee_text(self):
        response = Client().get("/coffee/")
        self.assertEqual(response.content.decode("utf-8"), "Я чайник")


__all__ = []
