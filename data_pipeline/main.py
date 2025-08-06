from fetch_tmdb import fetch_popular_movies, fetch_top_rated_movies, fetch_movies_by_genres
from normalize_data import normalize_movie_data
from insert_data import insert_movie

def run_pipeline():
    print("Accessing the TMDB API...")

    movies = (fetch_top_rated_movies() + fetch_popular_movies() + fetch_movies_by_genres())

    print(f"Fetched {len(movies)} movies")

    for movie in movies:
        normalized = normalize_movie_data(movie)
        insert_movie(normalized)
        print(f"Inserted/Updated: {normalized['title']}")
    print(f"Completed search for {len(movies)} TMDb movies")

if __name__ == "__main__":
    run_pipeline()