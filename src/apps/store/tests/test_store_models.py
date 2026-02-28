import pytest
from django.urls import reverse


# test string name of category
def test_category_str(product_category):
    assert product_category.__str__() == "django"


# test category url
def test_category_reverse(
    client, product_category
):  # here product_category is a fixture
    category = product_category  # get the built category from factories
    url = reverse("store:category_list", args=[category])  # build the reverse url
    response = client.get(url)
    assert response.status_code == 200


# test product type string name
def test_product_type_str(product_type):
    assert product_type.__str__() == "book"


# test prouct specification string name
def test_product_spec_str(product_specification):
    assert product_specification.__str__() == "pages"


# test product url
def test_product_url_resolve(client, product):
    slug = "product_slug"
    url = reverse("store:product_detail", args=[slug])
    response = client.get(url)
    assert response.status_code == 200


# test product string name
def test_product_str(product):
    assert product.__str__() == "product_title"


# test product specification value string
def test_product_spec_value_str(product_spec_value):
    assert product_spec_value.__str__() == "100"
