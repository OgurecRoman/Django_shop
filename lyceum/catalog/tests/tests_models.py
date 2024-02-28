import django.core.exceptions
import django.test
import parameterized

import catalog.models


class ModelsTests(django.test.TestCase):
    def setUp(self):
        self.category = catalog.models.Category.objects.create(
            name="Тестовая категория 1",
            slug="cat-slug-test",
        )
        self.tag = catalog.models.Tag.objects.create(
            is_published=True,
            name="Тестовый тег",
            slug="tag-slug-test",
        )

    def tearDown(self):
        catalog.models.Item.objects.all().delete()
        catalog.models.Tag.objects.all().delete()
        catalog.models.Category.objects.all().delete()

        super(ModelsTests, self).tearDown()

    @parameterized.parameterized.expand(
        [
            ("Превосходно",),
            ("роскошно",),
            ("роскошно!",),
            ("роскошно@",),
            ("!роскошно",),
            ("не роскошно",),
        ],
    )
    def test_item_validator(self, text):
        item_count = catalog.models.Item.objects.count()

        item = catalog.models.Item(
            name="Тестовый товар",
            text=text,
            category=self.category,
        )
        item.full_clean()
        item.save()
        item.tags.add(self.tag)

        self.assertEqual(
            catalog.models.Item.objects.count(),
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
        ],
    )
    def test_item_negative_validator(self, text):
        item_count = catalog.models.Item.objects.count()

        with self.assertRaises(django.core.exceptions.ValidationError):
            item = catalog.models.Item(
                name="Тестовый товар",
                text=text,
                category=self.category,
            )
            item.full_clean()
            item.save()

        self.assertEqual(
            catalog.models.Item.objects.count(),
            item_count,
        )

    @parameterized.parameterized.expand(
        [
            (-100,),
            (0,),
            (64000,),
        ],
    )
    def test_category_negative_validator(self, weight):
        category_count = catalog.models.Category.objects.count()

        with self.assertRaises(django.core.exceptions.ValidationError):
            test_category = catalog.models.Category(
                name="Тестовая категория",
                weight=weight,
                slug="test-cat",
            )
            test_category.full_clean()
            test_category.save()

        self.assertEqual(
            catalog.models.Category.objects.count(),
            category_count,
        )

    @parameterized.parameterized.expand(
        [
            (1,),
            (100,),
            (32000,),
        ],
    )
    def test_category_validator(self, weight):
        category_count = catalog.models.Category.objects.count()

        test_category = catalog.models.Category(
            name="Тестовая категория",
            weight=weight,
            slug="test-cat",
        )
        test_category.full_clean()
        test_category.save()

        self.assertEqual(
            catalog.models.Category.objects.count(),
            category_count + 1,
        )

    @parameterized.parameterized.expand(
        [
            ("тестовая категория 1",),
            ("Тестовая категория 1.",),
            ("!Тестовая категория 1!",),
            ("Тестовая категория1",),
            ("тестовая категория 1,",),
        ],
    )
    def test_category_negative_name(self, name):
        category_count = catalog.models.Category.objects.count()

        with self.assertRaises(django.core.exceptions.ValidationError):
            category = catalog.models.Category(
                name=name,
                slug="testslug",
            )
            category.full_clean()
            category.save()

        self.assertEqual(
            catalog.models.Category.objects.count(),
            category_count,
        )
