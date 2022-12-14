from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class CategorySave(BaseModel):
    name: str = Field(min_length=3, max_length=10)

    class Config:
        anystr_lower = True
        anystr_strip_whitespace = True


class Category(CategorySave):
    key: UUID = Field(default_factory=uuid4)
