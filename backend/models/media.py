from datetime import date
from pydantic import BaseModel, Field
from typing import Optional, Literal, Any


class CastDTO(BaseModel):
    role: str
    name: Optional[str] = None
    character_name: Optional[str] = None
    profile_path: Optional[str] = None

class MediaDTO(BaseModel):
    id: str
    title: Optional[str]
    description: Optional[str]
    release_date: Optional[date]
    poster_path: Optional[str]
    backdrop_path: Optional[str]
    is_movie: Optional[bool] = True
    similarity_score: Optional[float] = None
    genres: Optional[list[str]] = None
    cast: Optional[list[CastDTO]] = None
    bookmarked: Optional[bool] = False

class MediaSearchDTO(MediaDTO):
    user_rating: Optional[float] = None

class MediaResponse(BaseModel):
    media: list[MediaDTO]
    cursor: Optional[int] = None
    has_more: Optional[bool] = None

class SearchMediaResponse(BaseModel):
    media: list[MediaSearchDTO]

class Rating(BaseModel):
    media_id: str
    score: float

class RatingBatchRequest(BaseModel):
    clerk_id: str
    ratings: list[Rating]

class RatingBatchResponse(BaseModel):
    clerk_id: str
    ratings: list[Rating]

class DeleteRatingRequest(BaseModel):
    clerk_id: str
    media_id: str

class RecommendationRequest(BaseModel):
    clerk_id: str
    cursor: int = Field(default=0, ge=0)
    limit: int = Field(default=10, ge=1)
    page_number: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1)
    refresh: bool = Field(default=False)
    from_startup: bool = Field(default=False)

class FilterCondition(BaseModel):
    field: Literal["generic", "title", "release_date", "is_movie", "genre.name", "people.name", "people.character"]
    value: Any

class SearchQuery(BaseModel):
    filters: Optional[list[FilterCondition]] = None
    sort_by: Optional[str] = None
    sort_order: Optional[Literal["asc", "desc"]] = "asc"
    clerk_id: Optional[str] = None
    limit: Optional[int] = 20
    offset: Optional[int] = 0

class WatchLaterDeleteBatchRequest(BaseModel):
    clerk_id: str
    media_id: str

class WatchLaterBatchRequest(BaseModel):
    clerk_id: Optional[str] = None
    medias_id: list[str]

class WatchLaterBatchResponse(BaseModel):
    clerk_id: Optional[str] = None
    medias_id: list[str]

class WatchLaterRequest(BaseModel):
    clerk_id: str
    page_number: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1)
