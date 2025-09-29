from datetime import date
from pydantic import BaseModel
from typing import Optional

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
