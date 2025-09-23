#!/usr/bin/env python3
import unittest
from unittest.mock import patch, Mock
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

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)

class TestGetJson(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        mock_get.return_value.json.return_value = test_payload
        result = get_json(test_url)
        self.assertEqual(result, test_payload)
        mock_get.assert_called_once_with(test_url)

class TestMemoize(unittest.TestCase):

    @patch('__main__.memoize', lambda f: f)
    def test_memoize(self):
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        # Create a mock for the a_method
        mock_instance = Mock()
        mock_instance.a_method.return_value = 42

        # Patch the instance's method directly
        with patch.object(TestClass, 'a_method', new=mock_instance.a_method):
            test_obj = TestClass()

            # Call a_property twice
            result1 = test_obj.a_property()
            result2 = test_obj.a_property()

            # Assert that the result is correct
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # Assert that the underlying method was only called once
            test_obj.a_method.assert_called_once()