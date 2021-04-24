import pytest
from aioresponses import aioresponses

from users_api.clients import GitHubClient, GitHubRequestError

pytestmark = pytest.mark.asyncio


ERROR_STATUS = (400, 401, 404, 500, 504)


class TestGitHubClient:
    def setup_method(self, method):
        self.base_uri = GitHubClient._base_uri
        self.gh_client = GitHubClient("gph_123456")

    async def test_get_user_details_with_success(self, github_user_data):
        with aioresponses() as mock_response:
            mock_response.get(
                f"{self.base_uri}/users/test", payload=github_user_data
            )
            result = await self.gh_client.get_user_details("test")

        assert result == github_user_data

    @pytest.mark.parametrize("error_status", ERROR_STATUS)
    async def test_get_user_details_with_request_error(self, error_status):
        with aioresponses() as mock_response:
            url = f"{self.base_uri}/users/test"
            mock_response.get(url, status=error_status)

            with pytest.raises(GitHubRequestError) as error:
                await self.gh_client.get_user_details("test")

            expected_error = (
                f"GitHub request Error. Status: {error_status} - URL: {url}"
            )
            assert str(error.value) == expected_error

    async def test_get_user_repositories_with_success(
        self, github_user_repositories_data
    ):
        with aioresponses() as mock_response:
            mock_response.get(
                f"{self.base_uri}/users/test/repos?direction=desc&sort=updated",
                payload=github_user_repositories_data,
            )
            result = await self.gh_client.get_user_repositories("test")

        assert result == github_user_repositories_data

    @pytest.mark.parametrize("error_status", ERROR_STATUS)
    async def test_get_user_repositories_with_request_error(self, error_status):
        with aioresponses() as mock_response:
            url = f"{self.base_uri}/users/test/repos"
            mock_response.get(
                f"{url}?direction=desc&sort=updated", status=error_status
            )

            with pytest.raises(GitHubRequestError) as error:
                await self.gh_client.get_user_repositories("test")

            expected_error = (
                f"GitHub request Error. Status: {error_status} - URL: {url}"
            )
            assert str(error.value) == expected_error

    async def test_get_repository_commits_with_success(
        self, github_user_repository_commits_data
    ):
        with aioresponses() as mock_response:
            mock_response.get(
                f"{self.base_uri}/repos/testing/test/commits?per_page=5&page=1",
                payload=github_user_repository_commits_data,
            )
            result = await self.gh_client.get_repository_commits("testing/test")

        assert result == github_user_repository_commits_data

    @pytest.mark.parametrize("error_status", ERROR_STATUS)
    async def test_get_repository_commits_with_request_error(
        self, error_status
    ):
        with aioresponses() as mock_response:
            url = f"{self.base_uri}/repos/testing/test/commits"
            mock_response.get(f"{url}?per_page=5&page=1", status=error_status)

            with pytest.raises(GitHubRequestError) as error:
                await self.gh_client.get_repository_commits("testing/test")

            expected_error = (
                f"GitHub request Error. Status: {error_status} - URL: {url}"
            )
            assert str(error.value) == expected_error
