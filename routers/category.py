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

def is_category_id(category_id:int):
    if not session.get(Category, category_id):
        return False
    return True



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

# read 
@router.get('/{category_id}', response_model= CategoryBase)
def get_a_category(category_id:int):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category not found')
    return category

#CRUD = create, read, update, delete

# update
@router.put('/update/{category_id}', response_model= CategoryBase)
def update_a_category(category_id:int, category:CategoryBase):
    
    current_category = session.get(Category, category_id)
    if not current_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category not found')
    current_category.name = category.name
    session.add(current_category)
    session.commit()
    session.refresh(current_category)
    return current_category

@router.delete('/delete/{category_id}')
def delete_a_category(category_id:int):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category not found')
    session.delete(category)
    session.commit()
    return {'Deleted': category}