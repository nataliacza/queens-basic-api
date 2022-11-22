from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class UserId(BaseModel):
    key: UUID = Field(default_factory=uuid4)


class UserName(BaseModel):
    username: str = Field(min_length=5, max_length=20)


class UserBase(UserName):
    password: str = Field(min_length=5, max_length=20)


class UserSave(UserName, UserId):
    password: str


class User(UserName, UserId):
    pass


class UserLogin(BaseModel):
    username: str
    password: str


class AccessToken(BaseModel):
    token: str
