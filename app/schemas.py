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
    info: str | None
    on_stage_since: int | None
    hometown: City | None
    residence: City | None
    email: EmailStr | None
    web: HttpUrl | None
    instagram: HttpUrl | None
    facebook: HttpUrl | None
    twitter: HttpUrl | None
    tags: List[Category] = Field(default=[])


class QueenSave(BaseModel):
    nickname: str
    status: StatusEnum = Field(default=StatusEnum.Unknown)
    info: str | None
    on_stage_since: int | None
    hometown: UUID | None
    residence: UUID | None
    email: EmailStr | None
    web: HttpUrl | None
    instagram: HttpUrl | None
    facebook: HttpUrl | None
    twitter: HttpUrl | None
    tags: List[UUID] = Field(default=[])
