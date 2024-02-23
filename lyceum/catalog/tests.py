import itertools

import django.core
import django.test
from django.test import Client, TestCase
import parameterized

from . import models


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


class ModelsTests(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.category = models.Category.objects.create(
            is_published=True,
            name="Тестовая категория",
            slug="cat-slug-test",
            weight=100,
        )
        cls.tag = models.Tag.objects.create(
            is_published=True,
            name="Тестовый тег",
            slug="tag-slug-test",
        )

    def test_unable_create_without_prevosh(self):
        item_count = models.Item.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.item = models.Item(
                name="Тестовый товар",
                category=self.category,
                text="описание",
            )
            self.item.full_clean()
            self.item.save()
            self.item.tags.add(self.tag)

            self.assertEqual(models.Item.objects.count(), item_count)

    def test_unable_create_item(self):
        item_count = models.Item.objects.count()
        self.item = models.Item(
            name="Тестовый товар",
            category=self.category,
            text="превосходно",
        )
        self.item.full_clean()
        self.item.save()
        self.item.tags.add(self.tag)

        self.assertEqual(models.Item.objects.count(), item_count + 1)

    def test_unable_create_slug_error(self):
        item_count = models.Tag.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.tag = models.Tag(
                name="Тестовый тег",
                slug="описание",
            )
            self.tag.full_clean()
            self.tag.save()
            self.tag.add(ModelsTests.tag)

            self.assertEqual(models.Tag.objects.count(), item_count)

    def test_unable_create_slug(self):
        item_count = models.Tag.objects.count()
        self.tag = models.Tag(
            name="Тестовый тег",
            slug="aboba",
        )
        self.tag.full_clean()
        self.tag.save()

        self.assertEqual(models.Tag.objects.count(), item_count + 1)
