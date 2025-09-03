from typing import Dict, List

import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

def fetch_genres(media_type: str) -> Dict[str, int]:
    print(f"Fetching {media_type} genres...")
    params = {"api_key": API_KEY}
    response = requests.get(f"{BASE_URL}/genre/{media_type}/list", params=params)
    if response.status_code == 200:
        data = response.json()
        return {genre["name"]: genre["id"] for genre in data.get("genres", [])}
    else:
        print(f"Problems accessing the TMDB API...\n{response.status_code} - {response.text}")
        return {}

def fetch_from_endpoint(endpoint: str, params: Dict, pages: int = 1) -> List[Dict]:
    all_results = []
    for page in range(1, pages + 1):
        params["page"] = page
        response = requests.get(f"{BASE_URL}{endpoint}", params=params)
        if response.status_code == 200:
            data = response.json()
            all_results.extend(data.get("results", []))
        else:
            print(f"Problems accessing the TMDB API...\n{response.status_code} - {response.text}")
        time.sleep(0.25)
    return all_results

def fetch_top_rated_media(media_type: str, pages: int = 10) -> List[Dict]:
    print(f"Fetching top rated {media_type}s...")
    params = {
        "api_key": API_KEY,
        "sort_by": "vote_average.desc",
        "vote_count.gte": 100
    }
    return fetch_from_endpoint(f"/discover/{media_type}", params, pages)

def fetch_popular_media(media_type: str, pages: int = 5) -> List[Dict]:
    print(f"Fetching popular {media_type}s...")
    params = {"api_key": API_KEY}
    return fetch_from_endpoint(f"/{media_type}/popular", params, pages)

def fetch_media_by_genres(media_type: str, pages_by_genre: int = 5) -> List[Dict]:
    print(f"Fetching {media_type}s by genres...")
    all_media = []
    params = {"api_key": API_KEY}
    genres = fetch_genres(media_type)

    for genre, genre_id in genres.items():
        params["with_genres"] = str(genre_id)
        media = fetch_from_endpoint(f"/discover/{media_type}", params, pages_by_genre)
        all_media.extend(media)
    return all_media
