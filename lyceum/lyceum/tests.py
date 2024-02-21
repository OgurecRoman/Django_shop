from django.test import Client, override_settings, TestCase


class CatalogStaticURLTests(TestCase):
    @override_settings(ALLOW_REVERSE=True)
    def test_catalog_endpoint_true(self):
        contents = []
        for i in range(10):
            response = Client().get("/coffee/")
            contents.append(response.content.decode("utf-8"))
        self.assertIn("Я чайник", contents)
        self.assertEqual(contents.count("Я кинйач"), 1)

    @override_settings(ALLOW_REVERSE=False)
    def test_catalog_endpoint_const_false(self):
        contents = []
        for i in range(10):
            response = Client().get("/coffee/")
            contents.append(response.content.decode("utf-8"))
        self.assertIn("Я чайник", contents)
        self.assertNotIn("Я кинйач", contents)
