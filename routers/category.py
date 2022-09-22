from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from db.database import session
from db.models import Category, CategoryBase
from sqlmodel import select
from typing import List


router = APIRouter(
    prefix='/category',
    tags=['category']
)

def is_category_name(category_name:str):
    if session.exec(
        select(Category).where(Category.name == category_name)
        ).one_or_none():
        return True
    return False


# create
@router.post('/create', status_code= status.HTTP_201_CREATED, response_model= CategoryBase)
def create_category(category: CategoryBase):
    if is_category_name(category_name=category.name):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Category name esta en uso')
    new_category = Category(name= category.name)
    session.add(new_category)
    session.commit()
    session.refresh(new_category)
    return new_category

# read list all categories
@router.get('/all', response_model= List[CategoryBase])
def get_all_categories():
    statement = select(Category)
    result = session.exec(statement)
    categories = result.all()
    return categories
