#!/usr/bin/env python3
"""Unit tests for utils module"""

import unittest
from parameterized import parameterized
import utils


class TestAccessNestedMap(unittest.TestCase):
    """Tests for access_nested_map"""

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test KeyError is raised with correct message"""
        with self.assertRaises(KeyError) as context:
            utils.access_nested_map(nested_map, path)
        expected = f"'{path[-1]}'"
        self.assertEqual(str(context.exception), expected)
