def normalize_media_data(medias: list[dict], is_movie: bool):
    normalized_media = []
    normalized_medias_genres = []
    seen = set()

    for media in medias:
        mid = f'f{media['id']}' if is_movie else f's{media['id']}'
        if mid in seen:
            continue

        m = {
            "id": f'f{media["id"]}' if is_movie else f's{media["id"]}',
            "title": media["title"] if "title" in media else media["name"],
            "is_movie": is_movie,
            "description": media["overview"],
            "release_date": media["release_date"] if "release_date" in media else media["first_air_date"],
            "poster_path": media.get("poster_path"),
            "backdrop_path": media.get("backdrop_path"),
        }

        if m["release_date"] == '' or m["description"] == '':
            continue

        seen.add(mid)

        normalized_media.append(m)
        media_genres = normalize_media_genres(media, is_movie)
        normalized_medias_genres.extend(media_genres)

    return normalized_media, normalized_medias_genres, seen

def normalize_movie_details(movies_without_details, movie_details):
    movies_with_details = []
    for movie in movies_without_details:
        detail = [m for m in movie_details if m['id'] == int(movie['id'][1:])]
        detail = detail[0]
        movie['original_title'] = detail['original_title']
        movie['popularity'] = detail['popularity']
        movie['runtime'] = detail['runtime']
        movies_with_details.append(movie)

    return movies_with_details

def normalize_series_details(series_without_details, series_details):
    series_with_details = []
    for serie in series_without_details:
        detail = [s for s in series_details if s['id'] == int(serie['id'][1:])]
        detail = detail[0]
        serie['popularity'] = detail['popularity']
        serie['original_title'] = detail['original_name']
        serie['number_of_seasons'] = detail['number_of_seasons']
        serie['number_of_episodes'] = detail['number_of_episodes']
        series_with_details.append(serie)

    return series_with_details

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

def normalize_media_genres(media: dict, is_movie: bool) -> list[dict]:
    normalized_media_genres = []

    mid = f'f{media["id"]}' if is_movie else f's{media["id"]}'
    for genre_id in media["genre_ids"]:
        normalized_media_genres.append({"media_id": mid, "genre_id": genre_id})

    return normalized_media_genres

def normalize_credits(movie_credits: list[dict], tv_credits: list[dict], series_details):
    people = []
    seen = set()
    normalized_credits = []

    for media in movie_credits:
        cast_with_character = [
            person for person in media.get("cast", [])
            if "character" in person and person["character"]
        ][:12]

        for person in cast_with_character:
            normalized_credits.append({
                "media_id": f'f{media["id"]}',
                "people_id": person["id"],
                "character": person["character"],
                "role": "actor",
                "name": person["name"],
                "popularity": person['popularity']
            })
            if person["id"] not in seen:
                people.append({
                    "id": person["id"],
                    "name": person["name"],
                    "profile_path": person.get("profile_path"),
                })
                seen.add(person["id"])

        crew_filtered = [
            person for person in media.get("crew", [])
            if person.get("job") in ("Director") or person.get("department") in ("Writing")
        ]

        for person in crew_filtered:
            normalized_credits.append({
                "media_id": f'f{media["id"]}',
                "people_id": person["id"],
                "character": person["job"],
                "role": "Directing",
                "name": person["name"]
            })
            if person["id"] not in seen:
                people.append({
                    "id": person["id"],
                    "name": person["name"],
                    "profile_path": person.get("profile_path"),
                })
                seen.add(person["id"])
        
    for media in tv_credits:
        cast_with_character = [
            person for person in media.get("cast", [])
            if "character" in person and person["character"]
        ][:10]

        for person in cast_with_character:
            normalized_credits.append({
                "media_id": f's{media["id"]}',
                "people_id": person["id"],
                "character": person["character"],
                "role": "actor",
                "name": person["name"],
                "popularity": person['popularity']
            })
            if person["id"] not in seen:
                people.append({
                    "id": person["id"],
                    "name": person["name"],
                    "profile_path": person.get("profile_path"),
                })
                seen.add(person["id"])

        detail = [s for s in series_details if s['id'] == media['id']]
        print(detail[0]['tagline'], detail[0]['created_by'])
        print(series_details[0]['id'], series_details[0]['name'])
        print(media['id'])
        crew_filtered =  detail[0]['created_by'] 
        print(crew_filtered)

        for person in crew_filtered:
            normalized_credits.append({
                "media_id": f's{media["id"]}',
                "people_id": person["id"],
                "character": "Criador(a)",
                "role": "Creator",
                "name": person["name"]
            })
            if person["id"] not in seen:
                people.append({
                    "id": person["id"],
                    "name": person["name"],
                    "profile_path": person.get("profile_path"),
                })
                seen.add(person["id"])

    return people, normalized_credits
