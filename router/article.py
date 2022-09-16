from schemas import ArticleBase, ArticleDisplay
from fastapi import APIRouter, Depends
from db.database import get_db
from sqlalchemy.orm import Session
from db import db_article


router = APIRouter(
    prefix='/article',
    tags=['article']
)


@router.post('/', response_model=ArticleDisplay)
def create_article(request: ArticleBase, db: Session = Depends(get_db)):
    return db_article.create_article(db, request)

@router.get('/{id}')
def get_article(id:int, db: Session = Depends(get_db)):
    return {
        'data': db_article.get_article(db, id)
    }