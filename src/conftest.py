# global config for pytest
# implements fixtures used by tests
import pytest


@pytest.fixture(scope="module")
def test_fixture1():
    print("Run each test")
    return 1
