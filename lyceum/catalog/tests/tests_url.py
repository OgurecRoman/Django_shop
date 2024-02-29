from http import HTTPStatus
import itertools

import django.core.exceptions
import django.test
from django.test import Client, TestCase
import parameterized


class CatalogStaticURLTests(TestCase):
    def test_catalog_endpoint(self):
        response = Client().get("/catalog/")
        self.assertEqual(response.status_code, HTTPStatus.OK)

    @parameterized.parameterized.expand(
        [
            ("1", HTTPStatus.OK),
            ("100", HTTPStatus.OK),
            ("0", HTTPStatus.OK),
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

    @parameterized.parameterized.expand(
        [
            (x[0], x[1][0], x[1][1])
            for x in list(
                itertools.product(
                    [
                        "converter",
                        "re",
                    ],
                    [
                        ("1", HTTPStatus.OK),
                        ("100", HTTPStatus.OK),
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
                ),
            )
        ],
    )
    def test_catalog_conv_endpoint(self, prefix, url, expected_status):
        full_url = f"/catalog/{prefix}/{url}/"
        response = Client().get(full_url)
        self.assertEqual(response.status_code, expected_status)


__all__ = [
    CatalogStaticURLTests,
]
