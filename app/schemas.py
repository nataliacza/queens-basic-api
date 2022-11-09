from enum import Enum
from typing import List
from uuid import UUID

from pydantic import BaseModel, EmailStr, HttpUrl, Field


class StatusEnum(str, Enum):
    Active = "Active"
    Inactive = "Inactive"
    Unknown = "Unknown"


class City(BaseModel):
    city_id: UUID
    name: str
    region: str
    country: str


class CitySave(BaseModel):
    name: str
    region: str
    country: str


class Category(BaseModel):
    category_id: UUID
    name: str


class CategorySave(BaseModel):
    name: str


class Queen(BaseModel):
    queen_id: UUID
    nickname: str
    status: StatusEnum = Field(default=StatusEnum.Unknown)
    info: str = Field(default=None)
    on_stage_since: int = Field(default=None)
    hometown: City = Field(default=None)
    residence: City = Field(default=None)
    email: EmailStr = Field(default=None)
    web: HttpUrl = Field(default=None)
    instagram: HttpUrl = Field(default=None)
    facebook: HttpUrl = Field(default=None)
    twitter: HttpUrl = Field(default=None)
    tags: List[Category] = Field(default=[])


class QueenSave(BaseModel):
    nickname: str
    status: StatusEnum = Field(default=StatusEnum.Unknown)
    info: str = Field(default=None)
    on_stage_since: int = Field(default=None)
    hometown: UUID = Field(default=None)
    residence: UUID = Field(default=None)
    email: EmailStr = Field(default=None)
    web: HttpUrl = Field(default=None)
    instagram: HttpUrl = Field(default=None)
    facebook: HttpUrl = Field(default=None)
    twitter: HttpUrl = Field(default=None)
    tags: List[UUID] = Field(default=[])


class QueenBase(BaseModel):
    queen_id: UUID
    nickname: str
    status: StatusEnum = Field(default=StatusEnum.Unknown)
    on_stage_since: int = Field(default=None)
    tags: List[Category] = Field(default=[])
