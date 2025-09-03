def normalize_media_data(media, media_type, genres_map):
    genre_ids = media.get("genre_ids", [])
    genres = [genres_map.get(genre_id) for genre_id in genre_ids if genres_map.get(genre_id)]

    return {
        "id": media["id"],
        "title": media.get("title") or media.get("name"),
        "description": media.get("overview"),
        "release_date": media.get("release_date") or media.get("first_air_date"),
        "poster_path": media.get("poster_path"),
        "backdrop_path": media.get("backdrop_path"),
        "media_type": media_type,
        "genres": genres
    }