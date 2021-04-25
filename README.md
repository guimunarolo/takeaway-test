# Users API

A simple web application written in Python 3.8 with aiohttp that makes an interface with GitHub's API.


## How to run

Assuming that you already have docker and docker compose instaled, you'll need to add your GitHub access token to env vars:

    cp template.env .env

Then change the env `GITHUB_API_KEY` value with your access token.

> You just need to set repositories permissions to the token.
>
> [Instruction to create a personal access token](https://docs.github.com/pt/github/authenticating-to-github/creating-a-personal-access-token)

Now you just need to run:

    make run

The application is now running at [http://localhost:8080](http://localhost:8080).

Then you have the command `make logs` to see the application's logs and `make stop` to stop the container.


## Endpoints

### List users

List users with public repositories.

`GET /users`

**Parameters**

| Name       | Type   | In    | Description                                                                                       |
|------------|--------|-------|---------------------------------------------------------------------------------------------------|
|  usernames | list   | query | List of github's usernames separated by comma without spaces. Example: usernames=one,two,three    |
| include    | string | query | Flag to include the last public repository's commit. Value needs to be "commit_latest" (optional) |

**Response**

`Status: 200 OK`

```json
[
    {
        "login": "guimunarolo",
        "id": 8931516,
        "url": "https://api.github.com/users/guimunarolo",
        "public_repositories": [
            {
                "name": "postcode-validator-uk",
                "id": 238910669,
                "full_name": "guimunarolo/postcode-validator-uk",
                "created_at": "2020-02-07T11:54:26+00:00",
                "updated_at": "2020-11-22T19:35:11+00:00",
                "url": "https://api.github.com/repos/guimunarolo/postcode-validator-uk",
                "last_commit": {
                    "sha": "e43b2919a7d7e940ae072b24ab5d07587e8e3df8",
                    "author_email": "guimunarolo@hotmail.com",
                    "committer_email": "noreply@github.com",
                    "created_at": "2020-02-11T14:50:04+00:00",
                    "url": "https://api.github.com/repos/guimunarolo/postcode-validator-uk/commits/e43b2919a7d7e940ae072b24ab5d07587e8e3df8"
                }
            }
        ]
    }
]
```

> Response JSON schema: openapi/users-list-response-schema.json

`Status: 400 Bad Request`


## Running Tests

Just run:

    make test

You'll see the tests results and coverage.
