from typing import List

from pydantic import BaseModel, validator


class UsersParametersSerializer(BaseModel):
    usernames: List[str]
    include: str = None

    @validator("usernames", pre=True)
    def validate_and_split(cls, value):
        if not value:
            raise ValueError("empty value is not accepted")

        if isinstance(value, str):
            return value.split(",")

        return value
