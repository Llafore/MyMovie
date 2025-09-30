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

class Rating(BaseModel):
    media_id: int
    score: float

class RatingBatchRequest(BaseModel):
    clerk_id: str
    ratings: list[Rating]

class RatingBatchResponse(BaseModel):
    clerk_id: str
    ratings: list[Rating]

class RecommendationRequest(BaseModel):
    clerk_id: str
    limit: int = 10