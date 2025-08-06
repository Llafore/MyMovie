def normalize_movie_data(movie):
    return {
        "id": movie["id"],
        "title": movie["title"],
        "description": movie.get("overview"),
        "release_date": movie.get("release_date"),
        "poster_path": movie.get("poster_path"),
        "backdrop_path": movie.get("backdrop_path")
    }
