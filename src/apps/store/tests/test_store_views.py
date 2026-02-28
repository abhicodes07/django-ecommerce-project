import pytest
from django.urls import reverse


# provide this method a database
@pytest.mark.django_db
def test_root_url(client):
    url = reverse("store:product_all")
    response = client.get(url)
    assert response.status_code == 200
