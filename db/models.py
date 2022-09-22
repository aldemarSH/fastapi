from typing import Optional
from unicodedata import category
from sqlmodel import SQLModel, Field
from datetime import datetime

class CategoryBase(SQLModel):
    name: str = Field(min_length=3, max_length=20, index=True)

class Category(CategoryBase, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)

class VideoBase(SQLModel):
    title: str = Field(min_length=5, max_length=128, index= True)
    youtube_code:str =  Field(regex='[^ ]{11}')
    category_id: int = Field(foreign_key='category.id')

class Video(VideoBase, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    is_active: bool = Field(default=True)
    date_created: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    date_last_changed: Optional[datetime] = Field(default=None, nullable= True)