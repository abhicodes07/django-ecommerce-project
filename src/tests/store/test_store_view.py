import pytest


# mark test that its failing
# @pytest.mark.xfail
def test_hello_world3(test_fixture1):
    print("Function_fixture3")
    assert test_fixture1 == 1
