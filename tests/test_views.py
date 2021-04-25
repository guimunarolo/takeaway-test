from unittest import mock

import pytest

from users_api.exceptions import GitHubRequestError
from users_api.main import init_app


@pytest.fixture
def mock_get_users_from_api(user_data):
    return mock.AsyncMock(return_value=[user_data])


@pytest.fixture
def mock_service(mocker, mock_get_users_from_api):
    mock_service = mock.Mock()
    mock_service.get_users_from_api = mock_get_users_from_api
    mocker.patch("users_api.views.GitHubService", return_value=mock_service)
    return mock_service


class TestUserList:
    url = "/users"

    async def setup_client(self, aiohttp_client):
        app = await init_app()
        return await aiohttp_client(app)

    async def test_list_with_success(
        self, aiohttp_client, mock_service, mock_get_users_from_api, user_data
    ):
        client = await self.setup_client(aiohttp_client)
        response = await client.get(self.url, params={"usernames": "test"})

        assert response.status == 200
        assert await response.json() == [user_data]
        mock_get_users_from_api.assert_awaited_once_with(
            ["test"], include_last_commit=False
        )

    async def test_list_with_some_usernames(
        self, aiohttp_client, mock_service, mock_get_users_from_api, user_data
    ):
        client = await self.setup_client(aiohttp_client)
        response = await client.get(
            "/users", params={"usernames": "test,gvanrossum"}
        )

        assert response.status == 200
        assert await response.json() == [user_data]
        mock_get_users_from_api.assert_awaited_once_with(
            ["test", "gvanrossum"], include_last_commit=False
        )

    async def test_list_with_include_last_commit_parameter(
        self, aiohttp_client, mock_service, mock_get_users_from_api, user_data
    ):
        client = await self.setup_client(aiohttp_client)
        response = await client.get(
            "/users", params={"usernames": "test", "include": "commit_latest"}
        )

        assert response.status == 200
        assert await response.json() == [user_data]
        mock_get_users_from_api.assert_awaited_once_with(
            ["test"], include_last_commit=True
        )

    async def test_list_with_other_include_parameter(
        self, aiohttp_client, mock_service, mock_get_users_from_api, user_data
    ):
        client = await self.setup_client(aiohttp_client)
        response = await client.get(
            "/users", params={"usernames": "test", "include": "something"}
        )

        assert response.status == 200
        assert await response.json() == [user_data]
        mock_get_users_from_api.assert_awaited_once_with(
            ["test"], include_last_commit=False
        )

    async def test_list_without_usernames_parameter(
        self, aiohttp_client, mock_service, mock_get_users_from_api
    ):
        client = await self.setup_client(aiohttp_client)
        response = await client.get(self.url, params={})

        assert response.status == 400
        assert await response.json() == [
            {
                "loc": ["usernames"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
        mock_get_users_from_api.assert_not_awaited()

    async def test_list_with_service_error_raising(
        self, aiohttp_client, mock_service, mock_get_users_from_api
    ):
        error_msg = "error message"
        mock_get_users_from_api.side_effect = GitHubRequestError(error_msg)

        client = await self.setup_client(aiohttp_client)
        response = await client.get(self.url, params={"usernames": "test"})

        assert response.status == 400
        assert await response.json() == {"error": error_msg}
        mock_get_users_from_api.assert_awaited_once()
