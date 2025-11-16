    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test that KeyError is raised with correct message."""
        with self.assertRaises(KeyError) as context:
            utils.access_nested_map(nested_map, path)

        # Expected missing key is the last element in path
        expected_message = f"'{path[-1]}'"
        self.assertEqual(str(context.exception), expected_message)
