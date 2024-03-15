import django.test
import django.urls

import catalog.models


class CheckFieldsTestCase(django.test.TestCase):
    def check_content_value(self, item, exists, prefetched, not_loaded):
        check_dict = item.__dict__

        for value in exists:
            self.assertIn(value, check_dict)

        for value in prefetched:
            self.assertIn(value, check_dict["_prefetched_objects_cache"])

        for value in not_loaded:
            self.assertNotIn(value, check_dict)


class CatalogItemsTests(CheckFieldsTestCase):
    fixtures = ["fixtures/data.json"]

    def test_items_in_context(self):
        response = django.test.Client().get(
            django.urls.reverse("catalog:item_list"),
        )
        self.assertIn("items", response.context)

    def test_items_size(self):
        response = django.test.Client().get(
            django.urls.reverse("catalog:item_list"),
        )
        self.assertEqual(len(response.context["items"]), 5)

    def test_items_types(self):
        response = django.test.Client().get(
            django.urls.reverse("catalog:item_list"),
        )
        self.assertTrue(
            all(
                isinstance(
                    item,
                    catalog.models.Item,
                )
                for item in response.context["items"]
            ),
        )

    def test_items_loaded_values(self):
        response = django.test.Client().get(
            django.urls.reverse("catalog:item_list"),
        )
        for item in response.context["items"]:
            self.check_content_value(
                item,
                (
                    "name",
                    "text",
                    "category_id",
                ),
                ("tags",),
                (
                    "main_image",
                    "images",
                    "is_published",
                ),
            )


class DetailItemTests(CheckFieldsTestCase):
    fixtures = ["fixtures/data.json"]

    def test_items_in_context(self):
        response = django.test.Client().get(
            django.urls.reverse("catalog:item", args=[1]),
        )
        self.assertIn("item", response.context)

    def test_items_size(self):
        response = django.test.Client().get(
            django.urls.reverse("catalog:item", args=[1]),
        )
        self.assertIsInstance(
            response.context["item"],
            catalog.models.Item,
        )

    def test_items_loaded_values(self):
        response = django.test.Client().get(
            django.urls.reverse("catalog:item_list"),
        )
        self.check_content_value(
            response.context["item"],
            (
                "name",
                "text",
                "category_id",
            ),
            ("tags",),
            (
                "main_image",
                "images",
                "is_published",
            ),
        )
        self.check_content_value(
            response.context["item"].tags.all()[0],
            ("name",),
            (),
            ("is_published",),
        )


__all__ = []
