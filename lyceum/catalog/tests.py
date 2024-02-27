import itertools

import django.core.exceptions
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
    def setUp(self):
        self.category = models.Category.objects.create(
            name="Тестовая категория 1",
            slug="cat-slug-test",
        )
        self.tag = models.Tag.objects.create(
            is_published=True,
            name="Тестовый тег",
            slug="tag-slug-test",
        )

    def tearDown(self):
        models.Item.objects.all().delete()
        models.Tag.objects.all().delete()
        models.Category.objects.all().delete()

        super(ModelsTests, self).tearDown()

    @parameterized.parameterized.expand(
        [
            ("Превосходно",),
            ("роскошно",),
            ("роскошно!",),
            ("роскошно@",),
            ("!роскошно",),
            ("не роскошно",),
        ]
    )
    def test_item_validator(self, text):
        item_count = models.Item.objects.count()

        item = models.Item(
            name="Тестовый товар", text=text, category=self.category,
        )
        item.full_clean()
        item.save()
        item.tags.add(self.tag)

        self.assertEqual(
            models.Item.objects.count(),
            item_count + 1,
        )

    @parameterized.parameterized.expand(
        [
            ("Прев!осходно",),
            ("роскошный",),
            ("роскошное!",),
            ("оскошно@",),
            ("р оскошно",),
            ("qwertyроскошно",),
        ]
    )
    def test_item_negative_validator(self, text):
        item_count = models.Item.objects.count()

        with self.assertRaises(django.core.exceptions.ValidationError):
            item = models.Item(
                name="Тестовый товар", text=text, category=self.category,
            )
            item.full_clean()
            item.save()

        self.assertEqual(
            models.Item.objects.count(),
            item_count,
        )

    @parameterized.parameterized.expand(
        [
            (-100,),
            (0,),
            (64000,),
        ]
    )
    def test_category_negative_validator(self, weight):
        category_count = models.Category.objects.count()

        with self.assertRaises(django.core.exceptions.ValidationError):
            test_category = models.Category(
                name="Тестовая категория",
                weight=weight,
                slug="test-cat",
            )
            test_category.full_clean()
            test_category.save()

        self.assertEqual(
            models.Category.objects.count(),
            category_count,
        )

    @parameterized.parameterized.expand(
        [
            (1,),
            (100,),
            (32000,),
        ]
    )
    def test_category_validator(self, weight):
        category_count = models.Category.objects.count()

        test_category = models.Category(
            name="Тестовая категория",
            weight=weight,
            slug="test-cat",
        )
        test_category.full_clean()
        test_category.save()

        self.assertEqual(
            models.Category.objects.count(),
            category_count + 1,
        )
