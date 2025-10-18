import os
import sys

from dao.people_dao import PeopleDAO

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from fetch_tmdb import (fetch_popular_movies, fetch_top_rated_movies, fetch_genres, fetch_top_rated_series, fetch_popular_series,
                        fetch_series_by_genres, fetch_movies_by_genres, fetch_credits)
from normalize_data import normalize_media_data, normalize_genres, normalize_credits
from backend.dao.media_dao import MediaDAO
from backend.dao.genre_dao import GenreDAO

def search_genres():
    print("Fetching genres...")
    dao = GenreDAO()
    genres = fetch_genres()
    normalized_genre = normalize_genres(genres)
    dao.insert_genres(normalized_genre)

    print(f"Fetched {len(genres)} genres")
    return genres

def search_movies(genres: list[dict[int | str]] = None):
    print("Fetching movies...")
    dao = MediaDAO()
    movies = (fetch_top_rated_movies(pages=20) + fetch_popular_movies(pages=20) + fetch_movies_by_genres(genres, pages_by_genre=20))

    normalized_movies, normalized_movies_genres = normalize_media_data(movies, is_movie=True)


    dao.insert_media(normalized_movies)
    dao.insert_media_genres(normalized_movies_genres)

    print(f"Fetched {len(normalized_movies)} TMDb movies")

def search_series(genres: list[dict[int | str]] = None):
    print("Fetching series...")
    dao = MediaDAO()
    series = (fetch_top_rated_series(pages=20) + fetch_popular_series(pages=20) + fetch_series_by_genres(genres, pages_by_genre=20))

    normalized_series, normalized_series_genres = normalize_media_data(series, is_movie=False)

    dao.insert_media(normalized_series)
    dao.insert_media_genres(normalized_series_genres)

    print(f"Fetched {len(normalized_series)} TMDb series")

def search_credits():
    print("Fetching credits...")

    media_dao = MediaDAO()
    people_dao = PeopleDAO()

    movies_ids = media_dao.load_movies_ids()
    series_ids = media_dao.load_series_ids()
    credits = fetch_credits(movies_ids, series_ids)
    peoples, credits = normalize_credits(credits)

    people_dao.insert_people(peoples)
    people_dao.insert_credits(credits)

    return peoples, credits


def run_pipeline():
    print("Accessing the TMDB API...")
    genres = search_genres()
    search_movies(genres)
    search_series(genres)
    search_credits()
    print("Data pipeline done...")

if __name__ == "__main__":
    run_pipeline()
    # peoples, credits = search_credits()
    # print(peoples)