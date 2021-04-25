from aiohttp import web
from pydantic import ValidationError

from .exceptions import GitHubRequestError
from .serializers import UsersParametersSerializer
from .services import GitHubService


async def users_list(request):
    try:
        params = UsersParametersSerializer(**request.query)
    except ValidationError as exc:
        return web.json_response(exc.errors(), status=400)

    include_last_commit = params.include == "commit_latest"
    try:
        users = await GitHubService().get_users_from_api(
            params.usernames, include_last_commit=include_last_commit
        )
    except GitHubRequestError as exc:
        return web.json_response({"error": str(exc)}, status=400)

    return web.json_response(users)
