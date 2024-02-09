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
from unittest.mock import patch, PropertyMock
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

    def test_public_repos_url(self):
        """ Test that the public_repos_url is correct """
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            expected_url = "https://api.github.com/orgs/google/repos"
            mockPayload = {"repos_url": expected_url}
            # Set the return value of the mock object
            mock_org.return_value = mockPayload
            # Create an instance of GithubOrgClient
            github_client = GithubOrgClient("google")
            # Call the _public_repos_url method
            result = github_client._public_repos_url
            # Assert the result is of the expected repos_url from mock payload
            expected_result = mockPayload["repos_url"]
            self.assertEqual(result, expected_result)


@patch('client.GithubOrgClient._public_repos_url', new_callable=PropertyMock)
def test_public_repos(self, mock_public_repos_url):
    """Test public_repos method"""
    # Mocking the return value of _public_repos_url
    mock_public_repos_url.return_value = \
        "https://api.github.com/orgs/google/repos"
    # Mocking the return value of get_json
    with patch('client.get_json') as mock_get_json:
        mock_get_json.return_value = [{"name": "repo1"}, {"name": "repo2"}]
        # Creating an instance of GithubOrgClient
        github_org_client = GithubOrgClient("google")
        # Calling the public_repos method
        result = github_org_client.public_repos()
        # Expected result from the chosen payload
        expected_result = [{"name": "repo1"}, {"name": "repo2"}]
        # Asserting that the result matches the expected result
        self.assertEqual(result, expected_result)
        # Asserting that _public_repos_url was called once
        mock_public_repos_url.assert_called_once()
        # Asserting that get_json was called once
        mock_get_json.assert_called_once()
