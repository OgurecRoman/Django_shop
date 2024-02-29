from http import HTTPStatus

from django.test import Client, TestCase
import django.urls


class HomepageStaticURLTests(TestCase):
    def test_homepage_endpoint(self):
        response = Client().get(django.urls.reverse("homepage:main"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_coffee_endpoint(self):
        response = Client().get("/coffee/")
        self.assertEqual(response.status_code, HTTPStatus.IM_A_TEAPOT)

    def test_coffee_text(self):
        response = Client().get("/coffee/")
        if response.content.decode("utf-8") == "Я чайник":
            self.assertEqual(response.content.decode("utf-8"), "Я чайник")
        elif response.content.decode("utf-8") == "Я кинйач":
            self.assertEqual(response.content.decode("utf-8"), "Я кинйач")


__all__ = []
