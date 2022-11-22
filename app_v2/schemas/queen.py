import datetime
from typing import List
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, EmailStr, HttpUrl

from schemas.category import Category
from schemas.city import City
from schemas.enums import StatusEnum


def get_current_year():
    return datetime.datetime.utcnow().year


class QueenId(BaseModel):
    key: UUID = Field(default_factory=uuid4)


class QueenBase(QueenId):
    nickname: str = Field(min_length=2, max_length=40)
    status: StatusEnum = Field(default=StatusEnum.Unknown)
    on_stage_since: int = Field(default=None, le=get_current_year(), gt=get_current_year()-500)
    tags: List[Category] = Field(default=[], unique_items=True)


class QueenSocial(BaseModel):
    email: EmailStr = Field(default=None)
    web: HttpUrl = Field(default=None)
    instagram: HttpUrl = Field(default=None)
    facebook: HttpUrl = Field(default=None)
    twitter: HttpUrl = Field(default=None)


class Queen(QueenBase, QueenSocial, QueenId):
    nickname: str = Field(min_length=2, max_length=40)
    info: str = Field(default=None, max_length=500)
    hometown: City = Field(default=None)
    residence: City = Field(default=None)


class QueenSave(QueenSocial):
    nickname: str = Field(min_length=2, max_length=40)
    status: StatusEnum = Field(default=StatusEnum.Unknown)
    info: str = Field(default=None, max_length=500)
    on_stage_since: int = Field(default=None, le=get_current_year(), gt=get_current_year()-500)
    hometown: UUID = Field(default=None)
    residence: UUID = Field(default=None)
    tags: List[UUID] = Field(default=[], unique_items=True)
