from fastapi import APIRouter, Query, Path, Body
from pydantic import BaseModel
from typing import Optional, List
import time

router = APIRouter(prefix="/blog", tags=["blogs"])


class BlogModel(BaseModel):
    title: str
    content: str
    nb_comments: int
    published: Optional[bool]


@router.post("/new")
def create_blog(blog: BlogModel, id: int, version: int = 1):
    return {"id": id, "data": blog, "version": version}


@router.post("/new/{id}/comment")
def create_commit(
    blog: BlogModel,
    id: int = Path(None, description="esto es el id del blog", ge=5),
    comment_id: int = Query(
        None,
        title="esto es el Id del comentario",
        description="esto es una descripcion",
        deprecated=True,
        alias="commentID",
    ),
    content: str = Body(..., min_length=5, max_length=10),
    v: Optional[List[str]] = Body(["1", "2", "3"]),
):
    return {"blog": blog, "id": id, "comment_ID": comment_id, "content": content}

def required_funcionality():
    time.sleep(3)
    return {'mensaje':'me demore un poco'}