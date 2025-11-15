#!/usr/bin/env python3
"""Unit tests for utils.access_nested_map"""

import unittest
from parameterized import parameterized
import utils


class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map returns the expected output."""
        self.assertEqual(utils.access_nested_map(nested_map, path), expected)


    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_key):
        """Test KeyError is raised with correct message."""
        with self.assertRaises(KeyError) as err:
            utils.access_nested_map(nested_map, path)

        self.assertEqual(str(err.exception), f"'{expected_key}'")
