#!/usr/bin/env python3
import unittest
from utils import *
from parameterized import parameterized

class TestAccessNestedMap(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    @parameterized.expand([
    # Test case 1: simple key
    ({"a": 1}, ("a",), 1),
    # Test case 2: nested dictionary
    ({"a": {"b": 2}}, ("a",), {"b": 2}),
    # Test case 3: two-level nested key
    ({"a": {"b": 2}}, ("a", "b"), 2),])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)
    