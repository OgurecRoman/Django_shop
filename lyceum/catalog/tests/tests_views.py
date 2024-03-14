from http import HTTPStatus

from django.test import Client, TestCase
import django.urls


class CatalogViewsTests(TestCase):
    def test_catalog_endpoint(self):
        response = Client().get(django.urls.reverse("catalog:item_list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_catalog_new(self):
        response = Client().get(django.urls.reverse("catalog:new"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_catalog_friday(self):
        response = Client().get(django.urls.reverse("catalog:friday"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_catalog_unverified(self):
        response = Client().get(django.urls.reverse("catalog:unverified"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_about_endpoint_1(self):
        response = Client().get(django.urls.reverse("about:about"))
        self.assertEqual(response.status_code, HTTPStatus.OK)


__all__ = []
