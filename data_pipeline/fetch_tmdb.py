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
    ts = time.perf_counter()
    params = { "api_key": API_KEY }

    movie_response = requests.get(f"{BASE_URL}/genre/movie/list", params=params)
    tv_response = requests.get(f"{BASE_URL}/genre/tv/list", params=params)

    te = time.perf_counter()
    print("time fetching genres:", te-ts)
    return movie_response.json()["genres"] + tv_response.json()["genres"]

def fetch_media_from_endpoint(endpoint: str, params: Dict, pages: int = 1):
    all_movies = []
    for page in range(1, pages + 1):
        params["page"] = page
        response = requests.get(f"{BASE_URL}{endpoint}", params=params)
        if response.status_code == 200:
            data = response.json()
            all_movies.extend(data.get("results", []))
        else:
            print(f"Problems accessing the TMDB API...\n{response.status_code} - {response.text}")
    return all_movies

def fetch_top_rated_movies(pages: int = 10):
    ts = time.perf_counter()
    print("Fetching top rated movies...")
    movies = []
    params = { "api_key": API_KEY }

    url = f"/movie/top_rated?language={LANGUAGE}"
    movies.extend(fetch_media_from_endpoint(url, params, pages))
    print(len(movies))

    te = time.perf_counter()
    print("time fetching top rated movies:", te-ts)
    return movies

def fetch_popular_movies(pages: int = 10):
    ts = time.perf_counter()
    print("Fetching popular movies...")
    movies = []
    params = { "api_key": API_KEY }

    url = f"/movie/popular?language={LANGUAGE}"
    movies.extend(fetch_media_from_endpoint(url, params, pages))

    te = time.perf_counter()
    print("time fetching popular movies:", te-ts)
    return movies

def fetch_movies_by_genres(genres, pages_by_genre: int = 5):
    ts = time.perf_counter()
    print("Fetching movies by genres...")
    all_movies = []
    params = { "api_key": API_KEY }

    for genre  in genres:
        params["with_genres"] = str(genre["id"])
        movies = fetch_media_from_endpoint(f"/discover/movie?language={LANGUAGE}", params, pages_by_genre)
        all_movies.extend(movies)
    te = time.perf_counter()
    print("time fetching movies by genres:", te-ts)
    return all_movies

def fetch_top_rated_series(pages: int = 10):
    ts = time.perf_counter()
    print("Fetching top rated series...")
    series = []
    params = {"api_key": API_KEY}

    url = f"/tv/top_rated?language={LANGUAGE}"
    series.extend(fetch_media_from_endpoint(url, params, pages))

    te = time.perf_counter()
    print("time fetching top rated series:", te - ts)
    return series

def fetch_popular_series(pages: int = 10):
    ts = time.perf_counter()
    series = []
    print("Fetching popular series...")
    params = {"api_key": API_KEY}

    url = f"/tv/popular?language={LANGUAGE}"
    series.extend(fetch_media_from_endpoint(url, params, pages))

    te = time.perf_counter()
    print("time fetching popular series:", te - ts)
    return series

def fetch_series_by_genres(genres, pages_by_genre: int = 5):
    ts = time.perf_counter()
    print("Fetching series by genres...")
    all_series = []
    params = {"api_key": API_KEY}

    for genre in genres:
        params["with_genres"] = str(genre["id"])
        series = fetch_media_from_endpoint(f"/discover/tv?language={LANGUAGE}", params, pages_by_genre)
        all_series.extend(series)

    te = time.perf_counter()
    print("time fetching series by genres:", te - ts)
    return all_series

def fetch_movie_credits(movies_ids: list[dict[str|int]]):
    ts = time.perf_counter()
    all_credits = []
    params = { "api_key": API_KEY }

    for movie_id in movies_ids:
        url = f"{BASE_URL}/movie/{movie_id['id'][1:]}/credits"
        response = requests.get(url, params=params)
        all_credits.append(response.json())

    te = time.perf_counter()
    print("time fetching credits:", te-ts)
    return all_credits

def fetch_tv_credits(series_ids: list[int]):
    ts = time.perf_counter()
    all_credits = []
    params = { "api_key": API_KEY }

    for serie_id in series_ids:
        url = f"{BASE_URL}/tv/{serie_id['id'][1:]}/credits"
        response = requests.get(url, params=params)
        all_credits.append(response.json())

    te = time.perf_counter()
    print("time fetching credits:", te-ts)
    return all_credits
