import itertools

import django.test
from django.test import Client, TestCase
import parameterized


class CatalogStaticURLTests(TestCase):
    def test_catalog_endpoint(self):
        response = Client().get("/catalog/")
        self.assertEqual(response.status_code, 200)

    @parameterized.parameterized.expand(
        [
            ("1", 200),
            ("100", 200),
            ("0", 200),
            ("-0", 404),
            ("-100", 404),
            ("0.5", 404),
            ("abc", 404),
            ("0abc", 404),
            ("abc0", 404),
            ("$%^`", 404),
            ("1e5", 404),
        ]
    )
    def test_catalog_item_endpoint(self, url, expected_status):
        response = django.test.Client().get(f"/catalog/{url}/")
        self.assertEqual(response.status_code, expected_status)

    @parameterized.parameterized.expand(
        map(
            lambda x: (x[0], x[1][0], x[1][1]),
            itertools.product(
                [
                    "converter",
                    "re",
                ],
                [
                    ("1", 200),
                    ("100", 200),
                    ("0", 404),
                    ("-0", 404),
                    ("-100", 404),
                    ("0.5", 404),
                    ("abc", 404),
                    ("0abc", 404),
                    ("abc0", 404),
                    ("$%^`", 404),
                    ("1e5", 404),
                ],
            ),
        )
    )
    def test_catalog_conv_endpoint(self, prefix, url, expected_status):
        full_url = f"/catalog/{prefix}/{url}/"
        response = Client().get(full_url)
        self.assertEqual(response.status_code, expected_status)
