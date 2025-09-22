#!/usr/bin/env python3
import unittest
from utils import *
from parameterized import parameterized

class TestAccessNestedMap(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    @parameterized.expand([
    ({}, ("a",)),
    ({"a":1}, ("a","b")),])
    def test_access_nested_map_exception(self, nested_map, path):
        self.assertRaises(access_nested_map(nested_map, path))