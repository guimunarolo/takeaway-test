import pytest
from pydantic import ValidationError

from users_api.serializers import UsersParametersSerializer


class TestUsersParametersSerializer:
    def test_data_parsing(self):
        data = {"usernames": ["one", "two"], "include": "commit_latest"}
        params = UsersParametersSerializer(**data)

        assert params.usernames == data["usernames"]
        assert params.include == data["include"]

    def test_split_usernames(self):
        params = UsersParametersSerializer(usernames="one,two")

        assert params.usernames == ["one", "two"]

    @pytest.mark.parametrize(
        "invalid_data", ({}, {"usernames": None}, {"usernames": []})
    )
    def test_usernames_requirement(self, invalid_data):
        with pytest.raises(ValidationError) as exc:
            UsersParametersSerializer(**invalid_data)

        assert exc.value.errors()[0]["loc"] == ("usernames",)
