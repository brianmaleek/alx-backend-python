#!/usr/bin/env python3
"""
- Declare the TestGithubOrgClient(unittest.TestCase) class and implement the
    test_org method.
- This method should test that GithubOrgClient.org returns the correct value.
- Use @patch as a decorator to make sure get_json is called once with the
    expected argument but make sure it is not executed.
- Use @parameterized.expand as a decorator to parametrize the test with a
    couple of org examples to pass to GithubOrgClient, in this order:
        - google
        - abc
- Of course, no external HTTP calls should be made.
"""
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """ Test that json can be got """

    @parameterized.expand([
        ("google", {"google": True}),
        ("abc", {"abc": True})
    ])
    @patch('client.get_json')
    def test_org(self, org, expected_output, mock_get_json):
        """ Test the org of the client """
        mock_get_json.return_value = expected_output

        # Create an instance of GithubOrgClient
        github_client = GithubOrgClient(org)

        # Call the org method of the GithubOrgClient object
        result = github_client.org

        # Assert that the result is equal to the expected_output
        self.assertEqual(result, expected_output)

        # Assert that get_json was called once with the correct URL
        expected_url = f'https://api.github.com/orgs/{org}'
        mock_get_json.assert_called_once_with(expected_url)
