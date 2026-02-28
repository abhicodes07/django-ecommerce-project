import pytest


# test customer string
def test_customer_user(customer):
    assert customer.__str__() == "user1"


# test admin user
def test_admin_user(adminuser):
    assert adminuser.__str__() == "admin_user"


# test customer email when not entered
# should result in an error
def test_customer_email_no_input(customer_factory):
    # we expect an error so this test passes when it fails
    with pytest.raises(ValueError) as e:
        test = customer_factory.create(email="")
    assert str(e.value) == "Customer Account: You must provide an email address."


# test customer email when entered incorrect
# should result in an error
def test_customer_email_incorrect(customer_factory):
    # we expect an error so this test passes when it fails
    with pytest.raises(ValueError) as e:
        test = customer_factory.create(email="a.com")
    assert str(e.value) == "You must provide an email address"


# test admin email when not entered
# should result in an error
def test_admin_email_no_input(customer_factory):
    # we expect an error so this test passes when it fails
    with pytest.raises(ValueError) as e:
        test = customer_factory.create(email="", is_superuser=True, is_staff=True)
    assert str(e.value) == "Superuser Account: You must provide an email address."


# test admin email when not entered
# should result in an error
def test_admin_email_incorrect(customer_factory):
    # we expect an error so this test passes when it fails
    with pytest.raises(ValueError) as e:
        test = customer_factory.create(email="a.com", is_superuser=True, is_staff=True)
    assert str(e.value) == "You must provide an email address"


# test admin is_staff
# should result in an error
def test_admin_not_staff(customer_factory):
    # we expect an error so this test passes when it fails
    with pytest.raises(ValueError) as e:
        test = customer_factory.create(email="a.com", is_superuser=True, is_staff=False)
    assert str(e.value) == "Superuser must be assigned to is_staff=True."


# test admin is_superuser
def test_admin_not_superuser(customer_factory):
    # we expect an error so this test passes when it fails
    with pytest.raises(ValueError) as e:
        test = customer_factory.create(email="a.com", is_superuser=False, is_staff=True)
    assert str(e.value) == "Superuser must be assigned to is_superuser=True."


# test address string
def test_address_str(address):
    name = address.full_name
    assert address.__str__() == name + " Address"
