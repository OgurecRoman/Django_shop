from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse


class CatalogViewsTests(TestCase):
    def test_catalog_endpoint(self):
        reverse("catalog:item_list")
        response = Client().get("/catalog/")
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_catalog_endpoint_1(self):
        reverse("catalog:item", args=[1])
        response = Client().get("/catalog/1/")
        self.assertEqual(response.status_code, HTTPStatus.OK)


__all__ = [
    CatalogViewsTests,
]
