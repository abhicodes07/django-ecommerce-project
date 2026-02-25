from django.contrib.auth.models import User
from django.test import TestCase

from store.models import Category, Product


# test categories
class TestCatgoriesModel(TestCase):
    # add category data
    def setUp(self):
        # NOTE: here self is used because it allows other functions to access the below field

        # the data below should match correspoding columns in the model
        self.data1 = Category.objects.create(name="django", slug="django")

    def test_category_model_entry(self):
        """
        Test Category model data insertion/types/field attributes
        """

        data = self.data1

        # test if the data provided is of the same format as of the model
        self.assertTrue(isinstance(data, Category))

        # test the return name of the model
        # which is reutrn self.name
        self.assertEqual(str(data), "django")


# test products
class TestProductModel(TestCase):
    def setUp(self):
        Category.objects.create(name="django", slug="django")
        User.objects.create(username="admin")
        self.data1 = Product.objects.create(
            category_id=1,
            created_by_id=1,
            title="Ecommerce site with django",
            author="admin",
            slug="django-ecommerce",
            price="20.2",
            image="django",
        )

    def test_product_model_entry(self):
        """
        Test Category model data insertion/types/field attributes
        """
        data = self.data1
        self.assertTrue(isinstance(data, Product))
        self.assertEqual(str(data), "Ecommerce site with django")
