from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class CitySave(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    region: str = Field(min_length=3, max_length=50)
    country: str = Field(min_length=3, max_length=50)


class City(CitySave):
    key: UUID = Field(default_factory=uuid4)
