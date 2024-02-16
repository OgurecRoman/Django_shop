from django.test import Client, TestCase


class CatalogStaticURLTests(TestCase):
    def test_catalog_endpoint(self):
        response = Client().get("/catalog/")
        self.assertEqual(response.status_code, 200)

    def test_catalog_num_endpoint(self):
        response = Client().get("/catalog/", default="/1/")
        self.assertEqual(response.status_code, 200)

    def test_catalog_re_endpoint_1(self):
        response = Client().get("/catalog/", default="/re/1/")
        self.assertEqual(response.status_code, 200)

    def test_catalog_re_endpoint_1456(self):
        response = Client().get("/catalog/", default="/re/1456/")
        self.assertEqual(response.status_code, 200)

    def test_catalog_conv_endpoint_1(self):
        response = Client().get("/catalog/", default="/converter/1/")
        self.assertEqual(response.status_code, 200)

    def test_catalog_conv_endpoint_1234(self):
        response = Client().get("/catalog/", default="/converter/1234/")
        self.assertEqual(response.status_code, 200)
