from fetch_tmdb import fetch_popular_media, fetch_top_rated_media, fetch_media_by_genres, fetch_genres
from normalize_data import normalize_media_data
from insert_data import insert_media

def run_pipeline():
    print("Accessing the TMDB API...")

    movie_genres_map = fetch_genres("movie")
    tv_genres_map = fetch_genres("tv")

    genres_map = {v: k for k, v in movie_genres_map.items()}
    genres_map.update({v: k for k, v in tv_genres_map.items()})

    media = []
    for media_type in ["movie", "tv"]:
        media.extend(fetch_top_rated_media(media_type))
        media.extend(fetch_popular_media(media_type))
        media.extend(fetch_media_by_genres(media_type))

    print(f"Fetched {len(media)} media items")

    for item in media:
        media_type = "movie" if "title" in item else "tv"
        normalized = normalize_media_data(item, media_type, genres_map)
        insert_media(normalized)
        print(f"Inserted/Updated: {normalized['title']}")
    
    print(f"Completed search for {len(media)} TMDb media items")

if __name__ == "__main__":
    run_pipeline()