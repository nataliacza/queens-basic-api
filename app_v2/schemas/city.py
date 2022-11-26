from uuid import UUID, uuid4

from pydantic import BaseModel, Field, validator


class CitySave(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    region: str = Field(min_length=3, max_length=50)
    country: str = Field(min_length=3, max_length=50)

    @validator("name", "region", "country")
    def transform(cls, v: str):
        return v.title()

    class Config:
        anystr_strip_whitespace = True


class City(CitySave):
    key: UUID = Field(default_factory=uuid4)
