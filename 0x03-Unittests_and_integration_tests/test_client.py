#!/usr/bin/env python3
import unittest
from unittest.mock import patch, Mock
from utils import *
from client import *
from fixtures import TEST_PAYLOAD
from parameterized import parameterized, parameterized_class

class TestGithubOrgClient(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    @parameterized.expand([
        ("google", {"login": "google", "id": 1, "name": "Google"}),
        ("abc", {"login": "abc", "id": 2, "name": "ABC Corp"}),
    ])
    @patch('utils.get_json')
    def test_org(self, org_name, expected, mock_get_json):
        mock_get_json.return_value = expected
        client = GithubOrgClient(org_name)
        result = client.org
        self.assertEqual(result, expected)
        
        # Verify get_json was called once with correct URL
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url(self):
        mock_payload = {"repos_url": "https://api.github.com/orgs/testorg/repos"}
        
        # Use patch as context manager to mock org property
        with patch('client.GithubOrgClient.org', new_callable=Mock.PropertyMock) as mock_org:
            mock_org.return_value = mock_payload
            client = GithubOrgClient("testorg")
            result = client._public_repos_url
            self.assertEqual(result, mock_payload["repos_url"])
            mock_org.assert_called_once()

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        mock_repos = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get_json.return_value = mock_repos
        
        mock_url = "https://api.github.com/orgs/testorg/repos"
        with patch('client.GithubOrgClient._public_repos_url', new_callable=unittest.mock.PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = mock_url
            
            client = GithubOrgClient("testorg")
            result = client.public_repos
            
            expected = ["repo1", "repo2"]
            self.assertEqual(result, expected)
            
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(mock_url)
        
    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that GithubOrgClient.has_license returns the correct boolean."""
        client = GithubOrgClient("testorg")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)

@parameterized_class([
    {
        "org_name": "testorg",
        "org_payload": TEST_PAYLOAD[0][1][0]["id"].org_payload,
        "repos_payload": fixtures.repos_payload,
        "expected_repos": fixtures.expected_repos,
        "apache2_repos": fixtures.apache2_repos
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up class by mocking requests.get with fixtures."""
        def get_json_side_effect(url):
            if url == f"https://api.github.com/orgs/{cls.org_name}":
                return cls.org_payload
            if url == cls.org_payload["repos_url"]:
                return cls.repos_payload
            return None

        cls.get_patcher = patch('requests.get', return_value=Mock(json=Mock(side_effect=get_json_side_effect)))
        cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """Stop the patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test GithubOrgClient.public_repos returns expected repos."""
        client = GithubOrgClient(self.org_name)
        result = client.public_repos
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test GithubOrgClient.public_repos with license filter returns apache2 repos."""
        client = GithubOrgClient(self.org_name)
        result = client.public_repos(license="apache-2.0")
        self.assertEqual(result, self.apache2_repos)
