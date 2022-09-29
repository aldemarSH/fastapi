import sqlite3
from typing import Optional
from unicodedata import category
from sqlmodel import SQLModel, Field
from datetime import datetime

from pydantic import validator, EmailStr

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


class User(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    username: str = Field(index=True)
    password: str = Field(max_length=256, min_length=6)
    email: EmailStr
    created_at: datetime = datetime.now()
    is_creator: bool = False

class UserInput(SQLModel):
    username: str
    password: str = Field(max_length=256, min_length=6)
    password2: str
    email: EmailStr
    is_creator: bool = False

    @validator('password2')
    def password_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('password don\'t match')
        return v

class UserLogin(SQLModel):
    username: str
    password: str