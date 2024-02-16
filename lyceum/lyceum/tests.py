from django.test import Client, TestCase

contents = []


class CatalogStaticURLTests(TestCase):
    def test_catalog_endpoint(self):
        for i in range(10):
            response = Client().get("/coffee/")
            contents.append(response.content.decode("utf-8"))
        self.assertEqual(contents.count("Я кинйач"), 1)
