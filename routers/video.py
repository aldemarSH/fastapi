
from datetime import datetime
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from db.models import VideoBase, Video
from db.database import session
from routers.category import is_category_id
from sqlmodel import select 
from typing import List


router = APIRouter(
    prefix='/video',
    tags=['video']
)

def is_active_video(video_id:int):
    statement = select(Video).where(Video.id == video_id).where(Video.is_active)
    if session.exec(statement).one_or_none():
        return True
    return False


#create
@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=VideoBase)
def create_video(video: VideoBase):
    new_video = Video.from_orm(video)
    if not is_category_id(new_video.category_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    session.add(new_video)
    session.commit()
    session.refresh(new_video)
    return new_video

# read list all videos
@router.get('/all')
def get_all_videos():
    statement = select(Video).where(Video.is_active).order_by(Video.title)
    result = session.exec(statement)
    all_videos = result.all()
    return all_videos

# read a video
@router.get('/{video_id}', response_model=VideoBase)
def get_a_video(video_id:int):
    if not is_active_video(video_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No active video')
    video = session.get(Video, video_id)
    return video

#update
@router.put('/update/{video_id}', response_model=VideoBase)
def update_a_video(video_id:int, updated_video:VideoBase):
    if not is_active_video(video_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No active video')
    if not is_category_id(updated_video.category_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    original_video = session.get(Video, video_id)
    # obtener dicccionario e iterar sobre los campos, otra forma de actualizar
    # exclude_unset, excluye los valores que el usuario no modificó
    video_dict = updated_video.dict(exclude_unset=True)
    for key, value in video_dict.items():
        setattr(original_video, key, value)

    original_video.date_last_changed = datetime.utcnow()
    session.commit()
    session.refresh(original_video)
    return original_video
    
#delete
@router.delete('/delete/{video_id}')
def delete_a_video(video_id: int):
    if not is_active_video(video_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No active video')
    video = session.get(Video, video_id)
    video.is_active = False
    video.date_last_changed = datetime.utcnow()
    session.commit()
    return {'Deleted': video_id}

# undelete a video

@router.delete('/undelete/{video_id}')
def undelete_a_video(video_id: int):
    video = session.get(Video, video_id)
    if not video:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not exits')
    video.is_active = True
    video.date_last_changed = datetime.utcnow()
    session.commit()
    return {'Restored': video_id}
