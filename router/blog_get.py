import re
from fastapi import  Response, status, APIRouter, Depends
from enum import Enum
from typing import Optional
from router.blog_post import required_funcionality

router = APIRouter(
    prefix='/blog',
    tags=['blogs']
)

@router.get('/all', 
                    summary= 'este endpoint retorna todos los blogs', 
                    response_description='estos son los blogs')
def get_all_blogs(page=1, page_size: Optional[int] = None ):
    """_summary_

    Args:
        page (int, optional): _description_. Defaults to 1.
        page_size (Optional[int], optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """
    return {'mensaje': f' Todas las paginas de tamaño {page_size} en el blog con pagina {page}'}

@router.get('/{id}/comments/{comment_id}', tags=['comment'])
def get_comment(id: int, comment_id: int, valid: bool = True, username: Optional[str] = None):
    return {'mensaje': f'blog_id {id}, comment_id {comment_id}, valid {valid}, username {username}'}

class BlogType(str,Enum):
    short = 'short'
    story = 'story'
    howto = 'howto'

@router.get('/type/{type}')
def get_blog_type(type: BlogType, req_parameter: dict = Depends(required_funcionality)):
    return {'mensaje': f'Blog type {type}, {req_parameter}'}



@router.get('/{id}', status_code= status.HTTP_200_OK)
def get_blog(id: int, response: Response):
    if id > 5:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'mensaje': f'Blog no encontrado {id}'}
    else:
        response.status_code = status.HTTP_200_OK
        return {'mensaje': f'Blog con el id {id}'}