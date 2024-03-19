from http import HTTPStatus

import django.core.exceptions
import django.test
from django.test import Client, TestCase
import django.urls
import parameterized


class CatalogStaticURLTests(TestCase):
    fixtures = ["fixtures/data.json"]

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

    @parameterized.parameterized.expand(
        [
            ("1", HTTPStatus.OK),
            ("3", HTTPStatus.OK),
            ("0", HTTPStatus.NOT_FOUND),
            ("-0", HTTPStatus.NOT_FOUND),
            ("-100", HTTPStatus.NOT_FOUND),
            ("0.5", HTTPStatus.NOT_FOUND),
            ("abc", HTTPStatus.NOT_FOUND),
            ("0abc", HTTPStatus.NOT_FOUND),
            ("abc0", HTTPStatus.NOT_FOUND),
            ("$%^`", HTTPStatus.NOT_FOUND),
            ("1e5", HTTPStatus.NOT_FOUND),
        ],
    )
    def test_catalog_item_endpoint(self, url, expected_status):
        response = django.test.Client().get(f"/catalog/{url}/")
        self.assertEqual(response.status_code, expected_status)


__all__ = []
