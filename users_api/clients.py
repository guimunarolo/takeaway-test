from typing import Dict

from aiohttp import ClientSession

from .exceptions import GitHubRequestError


class GitHubClient:
    _access_token = None
    _base_uri = "https://api.github.com"

    async def __aenter__(self):
        self._session = ClientSession(headers=self._get_headers())
        return self

    async def __aexit__(self, *err):
        await self._session.close()
        self._session = None

    def __init__(self, access_token: str):
        self._access_token = access_token

    def _get_headers(self):
        return {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {self._access_token}",
        }

    async def _make_request(self, method, path, data={}, params={}):
        url = f"{self._base_uri}{path}"
        session_method = getattr(self._session, method)
        response = await session_method(url, json=data, params=params)
        if not response.ok:
            raise GitHubRequestError(
                f"GitHub request Error. Status: {response.status} - URL: {url}"
            )

        return await response.json()

    async def get_user_details(self, username: str) -> Dict:
        return await self._make_request("get", f"/users/{username}")

    async def get_user_repositories(self, username: str) -> Dict:
        params = {"sort": "updated", "direction": "desc"}
        url = f"/users/{username}/repos"
        return await self._make_request("get", url, params=params)

    async def get_repository_commits(
        self, repo_fullname: str, per_page: int = 5, page: int = 1
    ) -> Dict:
        params = {"per_page": per_page, "page": page}
        url = f"/repos/{repo_fullname}/commits"
        return await self._make_request("get", url, params=params)
