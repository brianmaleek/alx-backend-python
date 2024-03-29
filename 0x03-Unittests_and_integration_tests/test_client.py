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
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


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

    @patch("client.GithubOrgClient.org")
    def test_public_repos_url(self, mock_org_payload):
        """ Method to unit-test GithubOrgClient._public_repos_url """

        # Set up mock return value for GithubOrgClient.org
        mock_org_payload.return_value = {"repos_url": "url"}

        # Create instance of GithubOrgClient
        github_client = GithubOrgClient("repos_url")

        # Mocking GithubOrgClient._public_repos_url as a property
        with patch("client.GithubOrgClient._public_repos_url",
                   new_callable=PropertyMock) as mock_property:
            # Set the return value of the mocked property
            mock_property.return_value = mock_org_payload.\
                return_value["repos_url"]
            # Call _public_repos_url method
            result = github_client._public_repos_url

        # Assert the result
        self.assertEqual(result, "url")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """ Method to unit-test GithubOrgClient.public_repos """

        # Mock return value for get_json
        mock_get_json.return_value = [
            {"name": "value1"},
            {"name": "value2"}
        ]

        # Mocking GithubOrgClient._public_repos_url as a property
        with patch("client.GithubOrgClient._public_repos_url",
                   new_callable=PropertyMock) as mock_property:
            # Set the return value of the mocked property
            mock_property.return_value = "url"
            # Call public_repos method
            list_repos = GithubOrgClient("name").public_repos()

        # Define expected list of repositories
        expected_repos = ["value1", "value2"]

        # Assert the list of repos is as expected
        self.assertEqual(list_repos, expected_repos)

        # Assert that get_json was called once with the correct URL
        mock_get_json.assert_called_once_with("url")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """ Method to unit-test GithubOrgClient.has_license """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class(("org_payload", "repos_payload", "expected_repos", "apache2_repos"), TEST_PAYLOAD)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient"""

    @classmethod
    def setUpClass(TestSuite):
        """Set up class for integration tests"""
        # Patching requests.get to mock external requests
        TestSuite.get_patcher = patch('requests.get')
        TestSuite.mock_get = TestSuite.get_patcher.start()
        # Mocking the side effects of requests.get to return predefined payloads
        TestSuite.mock_get.side_effect = [
            Mock(json=Mock(return_value=TestSuite.org_payload)),
            Mock(json=Mock(return_value=TestSuite.repos_payload)),
        ]
        # Creating an instance of GithubOrgClient
        TestSuite.client = GithubOrgClient('google')

    @classmethod
    def tearDownClass(TestSuite):
        """Tear down class after integration tests"""
        # Stopping the patcher
        TestSuite.get_patcher.stop()

    def test_public_repos(TestSuite):
        """Test the public_repos method of GithubOrgClient"""
        # Call public_repos method without specifying a license
        result = TestSuite.client.public_repos()
        # Assert that the result matches the expected repositories
        TestSuite.assertEqual(result, TestSuite.expected_repos)

    def test_public_repos_with_license(TestSuite):
        """Test the public_repos method of GithubOrgClient with a license parameter"""
        # Call public_repos method with 'apache-2.0' license filter
        result = TestSuite.client.public_repos(license="apache-2.0")
        # Assert that the result matches the expected repositories with Apache 2.0 license
        TestSuite.assertEqual(result, TestSuite.apache2_repos)