from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from db.database import session
from sqlmodel import select
from typing import List
from routes.category import is_category_id
from datetime import datetime


from db.models import Video, VideoBase

router = APIRouter(
    prefix='/video',
    tags=['video']
)

# returns True if video id exists and is_active is True, otherwise returns False
def is_active_video(video_id:int):
    if session.exec(
            # Select where video id is valid and is_active is True
            select(Video).where(Video.id == video_id).where(Video.is_active)
        ).one_or_none():
        return True
    return False

#create
@router.post('/create', status_code= status.HTTP_201_CREATED, response_model=VideoBase)
def create_video(video:VideoBase):
    new_video = Video.from_orm(video)
    # Make sure new video has a valid video id
    if not is_category_id(new_video.category_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "No such category")
    session.add(new_video)
    session.commit()
    session.refresh(new_video)
    return new_video

# Get all active videos
@router.get('/all', response_model=List[Video])
def get_all_videos():
    # Include only videos where is_active is True
    statement = select(Video).where(Video.is_active).order_by(Video.title)
    result = session.exec(statement)
    all_videos = result.all()
    return all_videos

# Get one video, but only if it's active
@router.get('/{video_id}', response_model=VideoBase)
def get_a_video(video_id:int):
    # Return error if no active video with that id
    if not is_active_video(video_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "No active video with that id")
    video = session.get(Video, video_id)
    return video

@router.put('/update/{video_id}', response_model=VideoBase)
def update_a_video(video_id:int, updated_video:VideoBase):
    # Block if original video not there or inactive
    if not is_active_video(video_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "No such video")
    # Block if the new category id is no good
    if not is_category_id(updated_video.category_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Invalid category")
    # Otherwise, update the existing video to match updated_video

    # Get current video object from table
    original_video = session.get(Video,video_id)
    # Get dictionary so we can loop through fields
    video_dict = updated_video.dict(exclude_unset=True)
    # Loop is an alternative to doing each field on a separate line
    for key,value in video_dict.items():
        setattr(original_video, key,value)
    # Loop doesn't do date last changed, so we do that here
    original_video.date_last_changed = datetime.utcnow()
    session.commit()
    # After refresh, original video is the same as updated video
    session.refresh(original_video)
    return original_video

# Delete one video by changing is_active to False
@router.delete('/delete/{video_id}')
def delete_a_video(video_id:int):
    if not is_active_video(video_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "No such video")
    # Get the video to delete
    video = session.get(Video, video_id)
    # Set is_active to False, and update date last changed
    video.is_active = False
    video.date_last_changed = datetime.utcnow()
    session.commit()
    return {'Deleted':video_id}

# Undelete one video by changing is_active to True
@router.delete('/undelete/{video_id}')
def undelete_a_video(video_id:int):
    # Get the video to delete
    video = session.get(Video, video_id)
    if not video:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "No such video")
    # Set is_active to True, and update date last changed
    video.is_active = True
    video.date_last_changed = datetime.utcnow()
    session.commit()
    return {'Restored':video_id}