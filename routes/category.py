from fastapi.exceptions import HTTPException
from fastapi import APIRouter, status, Depends
from db.database import session
from sqlmodel import select
from typing import List
from routes.user import auth_handler

from db.models import Category, CategoryBase

router = APIRouter(
    prefix='/category',
    tags=['category']
    #dependencies=[Depends(auth_handler.auth_wrapper)]
)

def is_category_name(category_name:str):
    if session.exec(
        select(Category).where(Category.name == category_name)
        ).one_or_none():
        return True
    return False

def is_category_id(category_id:int):
    if not session.get(Category,category_id):
        return False
    return True

#create
@router.post('/create', status_code= status.HTTP_201_CREATED, response_model=CategoryBase)
def create_category(category:CategoryBase, user = Depends(auth_handler.auth_wrapper)):
    if is_category_name(category.name):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail='Category name is already in use')
    new_category = Category(name=category.name)
    session.add(new_category)
    session.commit()
    session.refresh(new_category)
    return new_category

#read list all categories
@router.get('/all', response_model=List[CategoryBase])
def get_all_categories():
    statement = select(Category).order_by(Category.name)
    result = session.exec(statement)
    categories = result.all()
    return categories

# read Get one category
@router.get('/{category_id}', response_model=CategoryBase)
def get_a_category(category_id:int):
    #Alternative syntax when getting one row by id
    category = session.get(Category, category_id)
    # Return error if no such category
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "No such category")
    return category

#Update
@router.put('/update/{category_id}', response_model=CategoryBase)
def update_a_category(category_id:int, category:CategoryBase):
    if not is_category_id(category_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "No such category")
    # Get current category object from table
    current_category = session.get(Category, category_id)
    # Replace current category name with the one just passed in
    current_category.name = category.name
    # Put back in table with new name
    session.add(current_category)
    session.commit()
    session.refresh(current_category)
    return current_category

# Delete one category
@router.delete('/delete/{category_id}')
def delete_a_category(category_id:int):
    if not is_category_id(category_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "No such category")
    # Don't allow them to delete category if it contains active videos
    #if count_videos_in_category(category_id) > 0:
    #    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Can't delete category that contains active videos")
    # Get the category to delete
    category = session.get(Category, category_id)
    # Delete the category
    session.delete(category)
    session.commit()
    return {'Deleted':category_id}
