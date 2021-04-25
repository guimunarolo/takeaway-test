import asyncio
from typing import Dict, List

from .clients import GitHubClient
from .configs import settings
from .models import Commit, Repository, User


class GitHubService:
    async def get_users_from_api(
        self, usernames: List, include_last_commit: bool = False
    ) -> List[Dict]:
        access_token = settings.GITHUB_API_KEY
        async with GitHubClient(access_token) as client_session:
            self._client_session = client_session

            tasks = (
                self._get_user_with_public_repositories(
                    username, include_last_commit
                )
                for username in usernames
            )

            return await asyncio.gather(*tasks)

    async def _get_user_with_public_repositories(
        self, username, include_last_commit
    ):
        user = await self._get_user(username)
        user.public_repositories = await self._get_user_public_repositories(
            username, include_last_commit
        )

        exclude = {}
        if not include_last_commit:
            exclude = {"public_repositories": {"__all__": {"last_commit"}}}

        return user.dict(exclude=exclude)

    async def _get_user(self, username):
        user_data = await self._client_session.get_user_details(username)
        return User.from_api_data(user_data)

    async def _get_user_public_repositories(
        self, username, include_last_commit
    ):
        repositories_data = await self._client_session.get_user_repositories(
            username
        )
        return await asyncio.gather(
            *(
                self._build_repository_obj(repository_data, include_last_commit)
                for repository_data in repositories_data
            )
        )

    async def _build_repository_obj(self, repository_data, include_last_commit):
        repo_obj = Repository.from_api_data(repository_data)
        if include_last_commit:
            repo_obj.last_commit = await self._get_latest_commit(
                repo_obj.full_name
            )

        return repo_obj

    async def _get_latest_commit(self, repository_full_name):
        commit_data = await self._client_session.get_repository_commits(
            repository_full_name, per_page=1
        )
        return Commit.from_api_data(commit_data[0])
