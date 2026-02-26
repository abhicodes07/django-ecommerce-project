# from django.test import TestCase
#
#
# class TestClass(TestCase):
#     def test_hello_world(self):
#         # match two strings
#         self.assertEqual("Hello", "Hello")
import pytest


def test_hello_world(test_fixture1):
    print("Function_fixture1")
    assert test_fixture1 == 1


def test_hello_world2(test_fixture1):
    print("Function_fixture2")
    assert test_fixture1 == 1
