#!/usr/bin/env python3
"""
- write the first unit test for utils.access_nested_map.
- Create a TestAccessNestedMap class that inherits from unittest.TestCase.
- Implement the TestAccessNestedMap.test_access_nested_map method to test that
    the method returns what it is supposed to.
- Decorate the method with @parameterized.expand to test the function for
    following inputs:
        - nested_map={"a": 1}, path=("a",)
        - nested_map={"a": {"b": 2}}, path=("a",)
        - nested_map={"a": {"b": 2}}, path=("a", "b")
- For each of these inputs, test with assertEqual that the function returns
    the expected result.
- The body of the test method should not be longer than 2 lines.
"""


import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json
from unittest.mock import patch, Mock
from typing import Dict, Any


class TestAccessNestedMap(unittest.TestCase):
    """
    A test class for the access_nested_map function in the utils module.
    """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected_result):
        """
        Test the access_nested_map function with various inputs.

        Parameters:
        - nested_map (dict): The nested dictionary to be accessed.
        - path (tuple): The path specifying the keys to access in the
            nested_map.
        - expected_result: The expected result when accessing the nested_map
            with the given path.
        """
        # Check if the access_nested_map function returns the expected result
        self.assertEqual(access_nested_map(nested_map, path), expected_result)

    @parameterized.expand([
        ({}, ("a",), KeyError, "'a'"),
        ({"a": 1}, ("a", "b"), KeyError, "'b'"),
    ])
    def test_access_nested_map_exception(self, nested_map, path,
                                         expected_exception, expected_message):
        """
        Test that access_nested_map raises a KeyError with expected message.

        Parameters:
        - nested_map (dict): The nested dictionary to be accessed.
        - path (tuple): The path specifying the keys to access the nested_map.
        - expected_exception (Exception): The expected exception class.
        - expected_message (str): The expected exception message.
        """
        with self.assertRaises(expected_exception) as context:
            access_nested_map(nested_map, path)

        # Check if the exception message matches the expected message
        self.assertEqual(expected_message, str(context.exception))


class TestGetJson(unittest.TestCase):
    """
    A test class for the get_json function in the utils module.
    """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('requests.get')
    def test_get_json(self, test_url: str, test_payload: Dict[str, Any],
                      mock_get: Mock) -> None:
        """
        Test the get_json function with various inputs.

        Parameters:
        - test_url (str): The URL to be used in the get_json function.
        - test_payload (dict): The payload to be returned by the mock get
            request.
        - mock_get (MagicMock): A mock of the requests.get function.
        """
        # Set the return value of the mock get request
        mock_get.return_value = Mock()
        mock_get.return_value.json.return_value = test_payload

        # Assert that the output of get_json is equal to test_payload
        self.assertEqual(get_json(test_url), test_payload)

        # Assert that the mocked get method was called exactly once with
        # test_url as argument
        mock_get.assert_called_once_with(test_url)
