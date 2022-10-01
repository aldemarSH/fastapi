from msilib.schema import tables
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

from pydantic import validator, EmailStr

class CategoryBase(SQLModel):
    name: str = Field(min_length=3, max_length=15, index=True)

class Category(CategoryBase, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)

# VideoBase (main user fields for Video table)
class VideoBase(SQLModel):
    title: str = Field(min_length=1,max_length=128,index=True)
    youtube_code: str = Field(regex='[^ ]{11}') # no puede tener espacios y debe contener 11 caracteres exactos
    # Link to Category model
    category_id: int = Field(foreign_key='category.id')

# Video class and sql table (includes VideoBase attributes)
class Video(VideoBase, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    # is_active is True (1) for normal rows, False (0) for deleted rows
    is_active: bool = Field(default=True)
    # Date this row was created, defaults to utc now
    date_created: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    # Date this row was last changed, defaults to None
    date_last_changed: Optional[datetime] = Field(default=None, nullable=True)


class User(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
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
            raise ValueError('passwords don\'t match')
        return v


class UserLogin(SQLModel):
    username: str
    password: str