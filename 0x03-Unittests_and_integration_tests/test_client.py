#!/usr/bin/env python3
import unittest
from unittest.mock import patch, Mock
from utils import *
from client import *
from fixtures import *
from parameterized import parameterized

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
    