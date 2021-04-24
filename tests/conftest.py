import pytest


@pytest.fixture
def commit_data():
    return {
        "sha": "d14a028c2a3a2bc9476102bb288234c415a2b01f828ea62ac5b3e42f",
        "author_email": "guimunarolo@hotmail.com",
        "committer_email": "guimunarolo@hotmail.com",
        "created_at": "2008-04-24T10:33:35Z",
        "url": "https://api.github.com/repos/guimunarolo/test/commits/hash",
    }


@pytest.fixture
def repository_data():
    return {
        "name": "test",
        "id": 1,
        "created_at": "2008-04-24T10:33:35Z",
        "updated_at": "2008-04-24T10:33:35Z",
        "url": "https://api.github.com/repos/guimunarolo/test",
    }


@pytest.fixture
def user_data():
    return {
        "login": "guimunarolo",
        "id": 1,
        "url": "https://api.github.com/users/guimunarolo",
    }
