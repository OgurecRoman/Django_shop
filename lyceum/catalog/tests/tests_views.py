from http import HTTPStatus

from django.test import Client, TestCase
import django.urls


class CatalogViewsTests(TestCase):
    def test_catalog_endpoint(self):
        response = Client().get(django.urls.reverse("catalog:item_list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_about_endpoint_1(self):
        response = Client().get(django.urls.reverse("about:about"))
        self.assertEqual(response.status_code, HTTPStatus.OK)


__all__ = []
