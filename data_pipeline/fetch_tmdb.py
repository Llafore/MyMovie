from typing import Dict

import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"
GENRES = {
    "Action": 28,
    "Comedy": 35,
    "Drama": 18,
    "Horror": 27,
    "Adventure": 12
}

def fetch_movies_from_endpoint(endpoint: str, params: Dict, pages: int = 1):
    all_movies = []
    for page in range(1, pages + 1):
        params["page"] = page
        response = requests.get(f"{BASE_URL}{endpoint}", params=params)
        if response.status_code == 200:
            data = response.json()
            all_movies.extend(data.get("results", []))
        else:
            print(f"Problems accessing the TMDB API...\n{response.status_code} - {response.text}")
        time.sleep(0.25)
    return all_movies

def fetch_top_rated_movies(pages: int = 10):
    print("Fetching top rated movies...")
    params = {
        "api_key": API_KEY,
        "sort_by": "vote_average.desc",
        "vote_count.gte": 100
    }

    return fetch_movies_from_endpoint("/discover/movie", params, pages)

def fetch_popular_movies(pages: int = 5):
    print("Fetching popular movies...")
    params = { "api_key": API_KEY }

    return fetch_movies_from_endpoint("/movie/popular", params, pages)

def fetch_movies_by_genres(pages_by_genre: int = 5):
    print("Fetching movies by genres...")
    all_movies = []
    params = { "api_key": API_KEY }

    for genre, genre_id in GENRES.items():
        params["with_genres"] = str(genre_id)
        movies = fetch_movies_from_endpoint("/discover/movie", params, pages_by_genre)
        all_movies.extend(movies)
    return all_movies