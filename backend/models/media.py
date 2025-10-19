from datetime import date
from pydantic import BaseModel, Field
from typing import Optional

class MediaDTO(BaseModel):
    id: int
    title: Optional[str]
    description: Optional[str]
    release_date: Optional[date]
    poster_path: Optional[str]
    backdrop_path: Optional[str]
    is_movie: Optional[bool] = True
    similarity_score: Optional[float] = None

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
    page_number: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1)
    refresh: bool = Field(default=False)
    from_startup: bool = Field(default=False)