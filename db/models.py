from typing import Optional
from sqlmodel import SQLModel, Field

class CategoryBase(SQLModel):
    name: str = Field(min_length=3, max_length=20, index=True)

class Category(CategoryBase, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)