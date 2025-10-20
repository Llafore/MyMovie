def normalize_media_data(medias: list[dict], is_movie: bool):
    normalized_media = []
    normalized_medias_genres = []
    seen = set()

    for media in medias:
        mid = media['id']
        if mid in seen:
            continue
        seen.add(mid)

        m = {
            "id": media["id"],
            "title": media["title"] if "title" in media else media["name"],
            "is_movie": is_movie,
            "description": media["overview"],
            "release_date": media["release_date"] if "release_date" in media else media["first_air_date"],
            "poster_path": media.get("poster_path"),
            "backdrop_path": media.get("backdrop_path"),
        }
        if m["release_date"] == '' or m["description"] == '':
            continue

        normalized_media.append(m)
        media_genres = normalize_media_genres(media)
        normalized_medias_genres.extend(media_genres)

    return normalized_media, normalized_medias_genres

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

def normalize_media_genres(media: dict) -> list[dict]:
    normalized_media_genres = []

    mid = media["id"]
    for genre_id in media["genre_ids"]:
        normalized_media_genres.append({"media_id": mid, "genre_id": genre_id})

    return normalized_media_genres

def normalize_credits(credits: list[dict]):
    peoples = []
    seen = set()
    normalized_credits = []

    for media in credits:
        cast_with_character = [
            person for person in media.get("cast", [])
            if "character" in person and person["character"]
        ][:15]

        for person in cast_with_character:
            normalized_credits.append({
                "media_id": media["id"],
                "people_id": person["id"],
                "character": person["character"],
                "role": "actor",
                "name": person["name"]
            })
            if person["id"] not in seen:
                peoples.append({
                    "id": person["id"],
                    "name": person["name"],
                    "profile_path": person.get("profile_path"),
                })
                seen.add(person["id"])

        crew_filtered = [
            person for person in media.get("crew", [])
            if person.get("job") in ("Executive Producer", "Director")
        ]

        for person in crew_filtered:
            normalized_credits.append({
                "media_id": media["id"],
                "people_id": person["id"],
                "character": None,
                "role": person["job"],
                "name": person["name"]
            })
            if person["id"] not in seen:
                peoples.append({
                    "id": person["id"],
                    "name": person["name"],
                    "profile_path": person.get("profile_path"),
                })
                seen.add(person["id"])

    return peoples, normalized_credits
