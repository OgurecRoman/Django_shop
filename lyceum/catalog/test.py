from django.test import Client, TestCase


class CatalogStaticURLTests(TestCase):

    def test_catalog_endpoint(self):
        response = Client().get("/catalog/")
        self.assertEqual(response.status_code, 200)

    def test_catalog_num_endpoint(self):
        response = Client().get("/catalog/", default="/1/")
        self.assertEqual(response.status_code, 200)
