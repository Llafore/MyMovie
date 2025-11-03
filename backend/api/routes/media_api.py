from datetime import datetime
from time import perf_counter
from typing import Dict
from fastapi import APIRouter, Query, status, HTTPException
from recommendation_engine.engine import Engine
from dao.media_dao import MediaDAO
from models.media import CastDTO, MediaDTO, MediaResponse, RatingBatchResponse, RatingBatchRequest, \
    RecommendationRequest, SearchQuery

import tracemalloc

from utils.media_util import MediaUtil

router = APIRouter(
    prefix='/media',
    tags=['Media'],
)

dao = MediaDAO()

tracemalloc.start()
recommendation_engine = Engine()
current, peak = tracemalloc.get_traced_memory()
print(f"Current memory usage: {current / 1024**2:.2f} MB")
print(f"Peak memory usage: {peak / 1024**2:.2f} MB")

tracemalloc.stop()

recommendation_cache: Dict[str, Dict] = {}
medias_startup_mock = ["f238", "s456", "f497", "s1396", "s1416", "s1429", "s2190", "s2316", "s14424", "s93405"]

@router.get('/media', response_model=MediaResponse)
def get_movies(page: int = Query(0, ge=0), page_size: int = Query(10, ge=1, le=100)):
    from_index = page * page_size
    to_index = (page + 1) * page_size - 1
    
    try:
        media_db_response = dao.load_media_paginated(from_index, to_index)
        media_dtos = [MediaDTO(**media) for media in media_db_response]

        filtered_media = [m for m in media_dtos if m.id not in medias_startup_mock] 
        return MediaResponse(media=filtered_media)

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


@router.get('/check_ratings')
def get_check_ratings(user: str):
    user_ratings = dao.get_ratings_by_clerk_id(user)
    if not user_ratings:
        raise HTTPException(status_code=404, detail="User reviews not found")
    return {"status": "ok"} 

@router.get('/startup_medias', response_model=MediaResponse)
def get_startup_medias():
    try:
        medias_dict = dao.get_medias(medias_startup_mock)
        medias_dtos = [MediaDTO(**media) for media in medias_dict]
        return MediaResponse(media=medias_dtos)
    except Exception as e:
        print(f"Error fetching startup medias: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching startup medias: {str(e)}")

@router.post('/recommendations', response_model=MediaResponse)
def get_recommendations(request: RecommendationRequest):
    try:
        clerk_id = request.clerk_id
        cursor = request.cursor
        limit = request.limit

        ts = perf_counter()
        user_ratings = dao.get_ratings_by_clerk_id(clerk_id)
        if not user_ratings:
            raise HTTPException(status_code=404, detail="User reviews not found")

        te = perf_counter()
        print(f"Time to fetch user ratings: {te - ts:0.4f} seconds")

        ts = perf_counter()
        user_ratings_dict = {
            rating['media_id']: rating['score']
            for rating in user_ratings
        }
        te = perf_counter()
        print(f"Time to build user ratings dict: {te - ts:0.4} seconds")


        ts = perf_counter()
        full_recommendation_series = recommendation_engine.recommend_media(
            user_history_scores=user_ratings_dict,
        )
        te = perf_counter()
        print(f"Time to generate recommendations: {te - ts:0.4f} seconds")

        ts = perf_counter()
        full_recommendation_ids = full_recommendation_series.index.tolist()
        recommendation_scores = full_recommendation_series.to_dict()
        te = perf_counter()
        print(f"Time to process recommendation results: {te - ts:0.4f} seconds")

        prev_seen = set()
        if not request.refresh and clerk_id in recommendation_cache:
            prev_seen = recommendation_cache[clerk_id].get("already_seen", set())

        already_seen = set() if request.refresh else prev_seen        

        recommendation_cache[clerk_id] = {
            "recommendation_ids": full_recommendation_ids,
            "recommendation_scores": recommendation_scores,
            "already_seen": already_seen,
            "timestamp": datetime.utcnow(),
        }

        cache = recommendation_cache[clerk_id]
        full_ids = cache["recommendation_ids"]
        already_seen = cache["already_seen"]  


        if (request.from_startup):
            filtered_ids = [mid for mid in full_ids if mid not in medias_startup_mock]
        else:
            filtered_ids = full_ids

        remaining = [mid for mid in filtered_ids if mid not in already_seen] 
        paged_ids = remaining[cursor : cursor + limit]
        # paged_ids = remaining[:page_size]

        cache["already_seen"].update(paged_ids)

        next_cursor = cursor + len(paged_ids)
        has_more = next_cursor < len(remaining)

        recommended_medias = dao.get_medias(paged_ids)

        ts = perf_counter()
        genres = dao.get_genres_from_medias(paged_ids)
        for media in recommended_medias:
            media['genres'] = [ 
                genre['genre']['name'] for genre in genres
                if genre['media_id'] == media['id']
            ]
        te = perf_counter()
        print(f"Time to fetch genres for recommended medias: {te - ts:0.4f} seconds")

        ts = perf_counter()
        credits = dao.get_credits_from_medias(paged_ids)
        for media in recommended_medias:
            media['cast'] = [ 
            CastDTO(
                role=credit['role'],
                name=credit['name'],
                character_name=credit['character'],
                profile_path=credit['people']['profile_path']
            )
            for credit in credits if credit['media_id'] == media['id']
        ]
        te = perf_counter()
        print(f"Time to fetch credits for recommended medias: {te - ts:0.4f} seconds")

        recommendation_series = recommendation_cache[clerk_id].get("recommendation_scores", {})
        
        media_by_id = {media["id"]: media for media in recommended_medias}
        
        ts = perf_counter()
        media_dtos = []
        for media_id in paged_ids:
            if media_id in media_by_id:
                media_dict = dict(media_by_id[media_id])
                media_dict["similarity_score"] = float(recommendation_series.get(media_id, 0))
                media_dtos.append(MediaDTO(**media_dict))
        te = perf_counter()
        print(f"Time to build MediaDTOs: {te - ts:0.4f} seconds")

        return MediaResponse(
            media=media_dtos,
            cursor=next_cursor,
            has_more=has_more,
        )

    except Exception as e:
        print(f"Error fetching recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching recommendations.")

@router.post('/search', response_model=MediaResponse)
def get_media_by_query(search: SearchQuery):
    try:
        medias_list = dao.load_by_query(search)
        media_dtos = MediaUtil.sql_to_dto(medias_list)

        return MediaResponse(media=media_dtos)
    except Exception as e:
        print(f"Error fetching search: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching query.")
