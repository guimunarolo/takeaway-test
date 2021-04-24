from datetime import datetime
from typing import Dict, List

from pydantic import BaseModel, validator


class Commit(BaseModel):
    sha: str
    author_email: str
    committer_email: str
    created_at: datetime
    url: str

    @validator("created_at")
    def datetime_to_isoformat(cls, value):
        return value.isoformat()

    @classmethod
    def from_api_data(cls, data: Dict) -> "Commit":
        return cls(
            sha=data["sha"],
            author_email=data["commit"]["author"]["email"],
            committer_email=data["commit"]["committer"]["email"],
            created_at=data["commit"]["committer"]["date"],
            url=data["url"],
        )


class Repository(BaseModel):
    name: str
    id: int
    full_name: str
    created_at: datetime
    updated_at: datetime
    url: str
    last_commit: Commit = {}

    @validator("created_at", "updated_at")
    def datetime_to_isoformat(cls, value):
        return value.isoformat()

    @classmethod
    def from_api_data(cls, data: Dict) -> "Repository":
        return cls(
            name=data["name"],
            id=data["id"],
            full_name=data["full_name"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            url=data["url"],
        )


class User(BaseModel):
    login: str
    id: int
    url: str
    public_repositories: List[Repository] = []

    @classmethod
    def from_api_data(cls, data: Dict) -> "User":
        return cls(login=data["login"], id=data["id"], url=data["url"])
