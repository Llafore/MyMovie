from fastapi import APIRouter, Query, status, HTTPException
from recommendation_engine.engine import Engine
from dao.media_dao import MediaDAO
from models.media import MediaDTO, MediaResponse, RatingBatchResponse, RatingBatchRequest, RecommendationRequest

from requests.models import Response

router = APIRouter(
    prefix='/media',
    tags=['Media'],
)

dao = MediaDAO()
recommendation_engine = Engine()

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

@router.post('/rating', response_model=RatingBatchResponse, status_code=status.HTTP_201_CREATED)
def post_rating(batch: RatingBatchRequest):
    try:
        new_rating = RatingBatchResponse(clerk_id=batch.clerk_id, ratings=batch.ratings)
        dao.insert_rating_by_batch(batch.clerk_id, batch.ratings)
        return new_rating
    except Exception as e:
        print(f"Error posting rating: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inserting reviews: {str(e)}")

@router.get('/startup_medias', response_model=MediaResponse)
def get_startup_medias():
    try:
        medias_startup_mock = [283, 456, 497, 1396, 1416, 1429, 2190, 2316, 14424, 93405]
        data = dao.get_medias(medias_startup_mock)
        media_dtos = [MediaDTO(**media) for media in data]
        return MediaResponse(media=media_dtos)
    except Exception as e:
        print(f"Error fetching startup medias: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching startup medias: {str(e)}")

@router.post('/recommendations', response_model=MediaResponse)
def get_recommendations(request: RecommendationRequest):
    try:
        user_ratings = dao.get_ratings_by_clerk_id(request.clerk_id)
        if not user_ratings:
            raise HTTPException(status_code=404, detail="User reviews not found")
        user_ratings_to_engine = {rating['media_id']: rating['score'] for rating in user_ratings}
        recommendations_series = recommendation_engine.recommend_media(past_recommendations=user_ratings_to_engine, top_n=request.limit)
        recommendations_ids = recommendations_series.index.tolist()
        recommendations_medias = dao.get_medias(recommendations_ids)
        media_dtos = [MediaDTO(**media) for media in recommendations_medias]
        return MediaResponse(media=media_dtos)
    except Exception as e:
        print(f"Error fetching recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching recommendations: {str(e)}")