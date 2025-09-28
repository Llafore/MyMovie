from datetime import date
import json
from typing import Optional
from fastapi import APIRouter, Query
from supabase_auth import BaseModel
from backend.dao.media_dao import MediaDAO

class MediaDTO(BaseModel):
    id: int
    title: Optional[str]
    description: Optional[str]
    release_date: Optional[date]
    poster_path: Optional[str]
    backdrop_path: Optional[str]
    is_movie: Optional[bool] = True

class MediaResponse(BaseModel):
    media: list[MediaDTO]

router = APIRouter(
    prefix='/media',
    tags=['Media'],
)

dao = MediaDAO()

@router.get('/media', response_model=MediaResponse)
def get_movies(page: int = Query(0, ge=0), page_size: int = Query(10, ge=1, le=100)):
    from_index = page * page_size
    to_index = (page + 1) * page_size - 1
    
    try:
        media_db_response = dao.load_media_paginated(from_index, to_index)
        media_dtos = [MediaDTO(**media) for media in media_db_response]
        return MediaResponse(media=media_dtos)
    except Exception as e:
        print(f"Error fetching media: {str(e)}")
        return MediaResponse(media=[])

    
