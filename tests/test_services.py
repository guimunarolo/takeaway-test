from unittest import mock

import pytest

from users_api.exceptions import GitHubRequestError
from users_api.services import GitHubService

pytestmark = pytest.mark.asyncio


@pytest.fixture
def mock_get_user_details(mocker, github_user_data):
    return mock.AsyncMock(return_value=github_user_data)


@pytest.fixture
def mock_get_user_repositories(mocker, github_user_repositories_data):
    return mock.AsyncMock(return_value=github_user_repositories_data)


@pytest.fixture
def mock_get_repository_commits(mocker, github_user_repository_commits_data):
    return mock.AsyncMock(return_value=github_user_repository_commits_data)


@pytest.fixture
def mock_client(
    mocker,
    mock_get_user_details,
    mock_get_user_repositories,
    mock_get_repository_commits,
):
    mock_client = mock.AsyncMock()
    mock_client.return_value.get_user_details = mock_get_user_details
    mock_client.return_value.get_user_repositories = mock_get_user_repositories
    mock_client.return_value.get_repository_commits = (
        mock_get_repository_commits
    )
    mocker.patch(
        "users_api.services.GitHubClient.__aenter__",
        side_effect=mock_client,
    )
    mocker.patch("users_api.services.GitHubClient.__aexit__")
    return mock_client


class TestGitHubService:
    async def test_get_users_from_api_without_include_last_commit(
        self,
        mock_client,
        mock_get_user_details,
        mock_get_user_repositories,
        mock_get_repository_commits,
        user,
        repository,
    ):
        user.public_repositories = [repository]
        user_data = user.dict()
        user_data["public_repositories"][0].pop("last_commit")

        username = user.login
        result = await GitHubService().get_users_from_api(
            usernames=[username], include_last_commit=False
        )

        assert result == [user_data]
        mock_get_user_details.assert_awaited_once_with(username)
        mock_get_user_repositories.assert_awaited_once_with(username)
        mock_get_repository_commits.assert_not_awaited()

    async def test_get_users_from_api_with_include_last_commit(
        self,
        mock_client,
        mock_get_user_details,
        mock_get_user_repositories,
        mock_get_repository_commits,
        user,
        repository,
        commit,
    ):
        repository.last_commit = commit
        user.public_repositories = [repository]
        user_data = user.dict()

        username = user.login
        result = await GitHubService().get_users_from_api(
            usernames=[username], include_last_commit=True
        )

        assert result == [user_data]
        mock_get_user_details.assert_awaited_once_with(username)
        mock_get_user_repositories.assert_awaited_once_with(username)
        mock_get_repository_commits.assert_awaited_once_with(
            repository.full_name, per_page=1
        )

    async def test_get_users_from_api_with_client_exception(self, mock_client):
        mock_client.side_effect = GitHubRequestError()

        with pytest.raises(GitHubRequestError):
            await GitHubService().get_users_from_api(usernames=["test"])
