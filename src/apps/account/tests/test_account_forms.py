import pytest
from apps.account.forms import RegistrationForm, UserAddressForm


# test form data
@pytest.mark.parametrize(
    "full_name, phone, address_line, address_line2, town_city, postcode, validity",
    [
        ("mike", "1234567890", "add1", "add2", "town", "postcode", True),
        ("", "1234567890", "add1", "add2", "town", "postcode", False),
    ],
)
def test_customer_add(
    full_name, phone, address_line, address_line2, town_city, postcode, validity
):
    form = UserAddressForm(
        data={
            "full_name": full_name,
            "phone": phone,
            "address_line": address_line,
            "address_line2": address_line2,
            "town_city": town_city,
            "postcode": postcode,
        }
    )

    assert form.is_valid() is validity


# test user creating multiple address
def test_customer_create_address(client, customer):
    user = customer
    client.force_login(user)
    response = client.post(
        "/account/add_address/",
        data={
            "full_name": "test",
            "phone": "test",
            "address_line": "test",
            "address_line2": "test",
            "town_city": "test",
            "postcode": "test",
        },
    )
    # 302 becuase in views we are redirecting user on successful
    # submission
    assert response.status_code == 302


# test RegistrationForm
@pytest.mark.parametrize(
    "user_name, email, password, password2, validity",
    # create a multiple test matrix to test multiple statements at once
    [
        ("test", "abhi@a.com", "#something123", "#something123", False),
        ("user1", "a12@a.com", "something123", "", False),  # no second password
        # ("user1", "a@a.com", "", "something123", False),  # no first password
        (
            "user1",
            "a12@a.com",
            "something123",
            "something124",
            False,
        ),  # password mismatch
        ("user1", "a12@.com", "something123", "something123", False),  # email
    ],
)
@pytest.mark.django_db  # we need database access for this
def test_create_account(user_name, email, password, password2, validity):
    form = RegistrationForm(
        data={
            "user_name": user_name,
            "email": email,
            "password": password,
            "password2": password2,
        },
    )
    assert form.is_valid() is validity


@pytest.mark.parametrize(
    "user_name, email, password, password2, validity",
    [
        ("user1", "a@a.com", "12345a", "12345a", 200),
        ("user1", "a@a.com", "12345a", "12345", 400),
        ("user1", "", "12345a", "12345", 400),
    ],
)
@pytest.mark.django_db
def test_create_account_view(client, user_name, email, password, password2, validity):
    response = client.post(
        "/account/register/",
        data={
            "user_name": user_name,
            "email": email,
            "password": password,
            "password2": password2,
        },
    )
    assert response.status_code == validity


def test_account_register_redirect(client, customer):
    user = customer
    client.force_login(user)
    response = client.get("/account/register/")
    assert response.status_code == 302


@pytest.mark.django_db
def test_account_register_render(client):
    response = client.get("/account/register/")
    assert response.status_code == 200
