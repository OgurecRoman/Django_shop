from django.test import Client, TestCase


class StaticURLTests(TestCase):
    def test_homepage_endpoint(self):
        response = Client().get("/")
        self.assertEqual(response.status_code, 200)

    def test_about_endpoint(self):
        response = Client().get("about/")
        self.assertEqual(response.status_code, 200)

    def test_catalog_endpoint(self):
        response = Client().get("catalog/")
        self.assertEqual(response.status_code, 200)

    def test_catalog_num_endpoint(self):
        response = Client().get("catalog/1/")
        self.assertEqual(response.status_code, 200)
