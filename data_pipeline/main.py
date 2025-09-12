from fetch_tmdb import fetch_popular_movies, fetch_top_rated_movies, fetch_movies_by_genres, fetch_genres
from normalize_data import normalize_movie_data
from insert_data import insert_movie, insert_genre

def search_genres():
    print("Fetching genres...")
    genres = fetch_genres()

    for genre in genres:
        insert_genre(genre)

    print(f"Fetched {len(genres)} genres")
    return genres

def search_movies(genres: list[dict[int | str]] = None):
    print("Fetching movies...")
    movies = (fetch_top_rated_movies() + fetch_popular_movies() + fetch_movies_by_genres(genres))

    for movie in movies:
        normalized = normalize_movie_data(movie)
        insert_movie(normalized)

    print(f"Fetched {len(movies)} TMDb movies")

def search_tv_shows():
    pass

def run_pipeline():
    print("Accessing the TMDB API...")
    genres = search_genres()
    search_movies(genres)
    search_tv_shows()
    print("Data pipeline done...")

if __name__ == "__main__":
    run_pipeline()