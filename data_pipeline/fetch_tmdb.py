from typing import Dict

import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"
LANGUAGE = "pt-BR"

def fetch_genres():
    params = {
        "api_key": API_KEY
    }

    movie_response = requests.get(f"{BASE_URL}/genre/movie/list", params=params)
    tv_response = requests.get(f"{BASE_URL}/genre/tv/list", params=params)

    return movie_response.json()["genres"] + tv_response.json()["genres"]

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
        "api_key": API_KEY
    }

    for page in range(1, pages + 1):
        url = f"/movie/top_rated?language={LANGUAGE}&page={page}"

    return fetch_movies_from_endpoint(url, params)

def fetch_popular_movies(pages: int = 10):
    print("Fetching popular movies...")
    params = { "api_key": API_KEY }

    return fetch_movies_from_endpoint("/movie/popular", params, pages)

def fetch_movies_by_genres(genres, pages_by_genre: int = 5):
    print("Fetching movies by genres...")
    all_movies = []
    params = { "api_key": API_KEY }

    for genre  in genres:
        params["with_genres"] = str(genre["id"])
        movies = fetch_movies_from_endpoint("/discover/movie", params, pages_by_genre)
        all_movies.extend(movies)
    return all_movies