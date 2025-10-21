from django.contrib.auth.models import User
from django.http import HttpRequest, request, response
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from store.models import Category, Product
from store.views import product_all


class TestViewResponses(TestCase):
    def setUp(self):
        """setup mock data"""
        # setup client to compose GET and POST request
        self.c = Client()
        self.factory = RequestFactory()

        # create a user
        User.objects.create(username="admin")
        Category.objects.create(name="django", slug="django")
        Product.objects.create(
            category_id=1,
            title="django beginners",
            slug="django-beginners",
            created_by_id=1,
            price=10.12,
            image="django",
            author="admin",
        )

    def test_url_allowed_hosts(self):
        """Test allowed hosts by simulating the browser."""

        response = self.c.get("/")

        # NOTE: here 200 status code means that the data Retrieval was successful
        self.assertEqual(response.status_code, 200)

    def test_product_detail_url(self):
        """Test product response status."""

        # test the reverse url
        response = self.c.get(
            reverse("store:product_detail", args=["django-beginners"])
        )

        # to check if it works or not change the response code to 100 or 300
        # as response.status_code returns status_code 200 if it matches ther second
        # operand then the test passes or it fails
        self.assertEqual(response.status_code, 200)

    def test_category_detail_url(self):
        """Test category response status"""

        response = self.c.get(reverse("store:category_list", args=["django"]))

        # NOTE: here 200 status code means that the data Retrieval was successfull
        self.assertEqual(response.status_code, 200)

    def test_homepage_html(self):
        """Test the homepage html"""
        request = HttpRequest()
        response = product_all(request)
        html = response.content.decode("utf-8")

        # below line says that the first argument should be contained by the second argument
        # self.assertIn("<title>Bookstore</title>", html)
        # self.assertTrue(html.startswith("\n<!doctype html>\n"))
        self.assertEqual(response.status_code, 200)

    def test_view_function(self):
        request = self.factory.get("/django-beginners")
        response = product_all(request)
        html = response.content.decode("utf8")

        # below line says that the first argument should be contained by the second argument
        self.assertIn("<summary>Library</summary>\n", html)
        self.assertEqual(response.status_code, 200)
