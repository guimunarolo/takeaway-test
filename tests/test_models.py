from users_api.models import Commit, Repository, User


def isoformat(datetime_str):
    return datetime_str.replace("Z", "+00:00")


class TestCommit:
    def test_data_parsing(self, commit_data):
        commit = Commit(**commit_data)

        assert commit.sha == commit_data["sha"]
        assert commit.author_email == commit_data["author_email"]
        assert commit.committer_email == commit_data["committer_email"]
        assert commit.created_at == isoformat(commit_data["created_at"])
        assert commit.url == commit_data["url"]

    def test_from_api_data_parsing(self, github_user_repository_commits_data):
        data = github_user_repository_commits_data[0]
        commit = Commit.from_api_data(data)

        assert commit.sha == data["sha"]
        assert commit.author_email == data["commit"]["author"]["email"]
        assert commit.committer_email == data["commit"]["committer"]["email"]
        assert commit.created_at == isoformat(
            data["commit"]["committer"]["date"]
        )
        assert commit.url == data["url"]


class TestRepository:
    def test_data_parsing(self, repository_data):
        repo = Repository(**repository_data)

        assert repo.name == repository_data["name"]
        assert repo.id == repository_data["id"]
        assert repo.full_name == repository_data["full_name"]
        assert repo.created_at == isoformat(repository_data["created_at"])
        assert repo.updated_at == isoformat(repository_data["updated_at"])
        assert repo.url == repository_data["url"]
        assert repo.last_commit == {}

    def test_last_commit_parsing(self, repository_data, commit_data):
        repository_data["last_commit"] = commit_data
        repo = Repository(**repository_data)

        assert isinstance(repo.last_commit, Commit) is True

    def test_from_api_data_parsing(self, github_user_repositories_data):
        data = github_user_repositories_data[0]
        repo = Repository.from_api_data(data)

        assert repo.name == data["name"]
        assert repo.id == data["id"]
        assert repo.full_name == data["full_name"]
        assert repo.created_at == isoformat(data["created_at"])
        assert repo.updated_at == isoformat(data["updated_at"])
        assert repo.url == data["url"]


class TestUser:
    def test_data_parsing(self, user_data):
        user = User(**user_data)

        assert user.login == user_data["login"]
        assert user.id == user_data["id"]
        assert user.url == user_data["url"]
        assert user.public_repositories == []

    def test_public_repositories_parsing(self, user_data, repository_data):
        user_data["public_repositories"] = [repository_data]
        user = User(**user_data)

        assert isinstance(user.public_repositories[0], Repository) is True

    def test_from_api_data_parsing(self, github_user_data):
        user = User.from_api_data(github_user_data)

        assert user.login == github_user_data["login"]
        assert user.id == github_user_data["id"]
        assert user.url == github_user_data["url"]
