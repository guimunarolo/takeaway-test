from datetime import datetime
from typing import List

from pydantic import BaseModel


class Commit(BaseModel):
    sha: str
    author_email: str
    committer_email: str
    created_at: datetime
    url: str


class Repository(BaseModel):
    name: str
    id: int
    created_at: datetime
    updated_at: datetime
    url: str
    last_commit: Commit = {}


class User(BaseModel):
    login: str
    id: int
    url: str
    public_repositories: List[Repository] = []
