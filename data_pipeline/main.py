import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from fetch_tmdb import (fetch_popular_movies, fetch_top_rated_movies, fetch_movies_by_genres,
                        fetch_genres, fetch_top_rated_series, fetch_popular_series ,
                        fetch_series_by_genres, fetch_movies_by_genres)
from normalize_data import normalize_media_data, normalize_genres, normalize_media_genres
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
    movies = (fetch_top_rated_movies(pages=1) + fetch_popular_movies(pages=1) + fetch_movies_by_genres(genres, pages_by_genre=1))

    normalized_media, normalized_medias_genres = normalize_media_data(movies, is_movie=True)

    dao.insert_media(normalized_media)
    dao.insert_media_genres(normalized_medias_genres)

    print(f"Fetched {len(normalized_media)} TMDb movies")

def search_series(genres: list[dict[int | str]] = None):
    print("Fetching series...")
    dao = MediaDAO()
    series = (fetch_top_rated_series(pages=1) + fetch_popular_series(pages=1) + fetch_series_by_genres(genres, pages_by_genre=1))

    normalized_series, normalized_medias_genres = normalize_media_data(series, is_movie=False)

    dao.insert_media(normalized_series)
    dao.insert_media_genres(normalized_medias_genres)

    print(f"Fetched {len(normalized_series)} TMDb series")


def run_pipeline():
    print("Accessing the TMDB API...")
    genres = search_genres()
    search_movies(genres)
    search_series(genres)
    print("Data pipeline done...")

if __name__ == "__main__":
    run_pipeline()