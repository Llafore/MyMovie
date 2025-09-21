def normalize_media_data(medias: list[dict], is_movie: bool) -> list[dict]:
    normalized_media = []
    seen = set()

    for media in medias:
        mid = media['id']
        if mid in seen:
            continue
        seen.add(mid)

        m = {
            "id": media["id"],
            "title": media["title"],
            "is_movie": is_movie,
            "release_date": media.get("release_date"),
            "poster_path": media.get("poster_path"),
            "backdrop_path": media.get("backdrop_path"),
        }
        if m["release_date"] == '': m["release_date"] = None

        normalized_media.append(m)

    return normalized_media

def normalize_genres(genres: list[dict[int | int]]) -> list[dict]:
    normalized_genres = []
    seen = set()

    for genre in genres:
        gid = genre["id"]
        if gid in seen:
            continue
        seen.add(gid)
        normalized_genres.append(genre)

    return normalized_genres

def normalize_media_genres(medias: list[dict]) -> list[dict]:
    normalized_media_genres = []

    for media in medias:
        mid = media["id"]
        for genre_id in media["genre_ids"]:
            normalized_media_genres.append({"media_id": mid, "genre_id": genre_id})

    return normalized_media_genres