import os
import sys
from time import perf_counter

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from fetch_tmdb import (fetch_movie_details, fetch_movies_by_genres, fetch_popular_movies, fetch_serie_details, fetch_series_by_genres, 
                        fetch_top_rated_movies, fetch_genres, fetch_top_rated_series, 
                        fetch_popular_series, fetch_movie_credits, fetch_tv_credits)
from normalize_data import (normalize_media_data, normalize_genres, normalize_credits, 
                            normalize_movie_details, normalize_series_details)
from backend.dao.media_dao import MediaDAO
from backend.dao.genre_dao import GenreDAO
from backend.dao.people_dao import PeopleDAO


class DataPipeline:
    
    def __init__(self):
        self.media_dao = MediaDAO()
        self.genre_dao = GenreDAO()
        self.people_dao = PeopleDAO()
        
        self.genres = []
        self.movies = []
        self.movies_ids = set()
        self.movie_genres = []
        self.series = []
        self.series_ids = set()
        self.series_genres = []
    
    def clear_data(self):
        print("Clearing data...")
        self.media_dao.clear_media_genres()
        self.people_dao.clear_people()
        self.people_dao.clear_credits()
        self.genre_dao.clear_genres()
        self.media_dao.clear_media()
    
    def fetch_genres(self):
        print("Fetching genres...")
        self.genres = fetch_genres()
        normalized_genre = normalize_genres(self.genres)
        self.genre_dao.insert_genres(normalized_genre)
        print(f"Fetched {len(self.genres)} genres")
    
    def fetch_movies(self):
        print("Fetching movies...")
        movies = (fetch_top_rated_movies(pages=15) + fetch_popular_movies(pages=8) + fetch_movies_by_genres(self.genres, pages_by_genre=2))
        self.movies, self.movie_genres, self.movies_ids = normalize_media_data(movies, is_movie=True)
        print(f"Fetched {len(self.movies)} TMDb movies")
    
    def fetch_series(self):
        print("Fetching series...")
        series = (fetch_top_rated_series(pages=15) + fetch_popular_series(pages=8) + fetch_series_by_genres(self.genres, pages_by_genre=2))
        self.series, self.series_genres, self.series_ids = normalize_media_data(series, is_movie=False)
        print(f"Fetched {len(self.series)} TMDb series")
    
    def fetch_and_store_credits(self):
        print("Fetching credits...")
        
        movie_credits = fetch_movie_credits(self.movies_ids)
        movie_details = fetch_movie_details(self.movies_ids)
        tv_credits = fetch_tv_credits(self.series_ids)
        series_details = fetch_serie_details(self.series_ids)
        
        movies_normalized = normalize_movie_details(self.movies, movie_details)
        self.media_dao.insert_media(movies_normalized)
        self.media_dao.insert_media_genres(self.movie_genres)
        
        series_normalized = normalize_series_details(self.series, series_details)
        self.media_dao.insert_media(series_normalized)
        self.media_dao.insert_media_genres(self.series_genres)
        
        ts = perf_counter()
        peoples, credits = normalize_credits(movie_credits, tv_credits, series_details)
        te = perf_counter()
        print(f"Time normalizing credits: {te-ts:.2f}s")
        
        self.people_dao.insert_people(peoples)
        self.people_dao.insert_credits(credits)
    
    def run(self):
        print("Accessing the TMDB API...")
        self.clear_data()
        self.fetch_genres()
        self.fetch_movies()
        self.fetch_series()
        self.fetch_and_store_credits()
        print("Data pipeline done...")


def run_pipeline():
    pipeline = DataPipeline()
    pipeline.run()


if __name__ == "__main__":
    ts = perf_counter()
    run_pipeline()
    te = perf_counter()
    print(f"Total time data pipeline: {te - ts:.2f}s")