from db_connection import get_connection

def insert_media(media):
    conn = get_connection()
    cursor = conn.cursor()

    for genre_name in media.get("genres", []):
        if genre_name:
            cursor.execute("INSERT IGNORE INTO genres (name) VALUES (%s)", (genre_name,))
    conn.commit()

    genre_ids = []
    for genre_name in media.get("genres", []):
        if genre_name:
            cursor.execute("SELECT id FROM genres WHERE name = %s", (genre_name,))
            result = cursor.fetchone()
            if result:
                genre_ids.append(result[0])

    release_date = media.get("release_date")
    if not release_date or str(release_date).strip() == "":
        release_date = None

    sql = (
        "INSERT INTO media (id, title, description, release_date, poster_path, backdrop_path, media_type) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s) "
        "ON DUPLICATE KEY UPDATE "
        "title = VALUES(title), "
        "description = VALUES(description), "
        "release_date = VALUES(release_date), "
        "poster_path = VALUES(poster_path), "
        "backdrop_path = VALUES(backdrop_path), "
        "media_type = VALUES(media_type)"
    )

    values = (
        media["id"],
        media["title"],
        media["description"],
        release_date,
        media["poster_path"],
        media["backdrop_path"],
        media["media_type"]
    )

    cursor.execute(sql, values)
    conn.commit()

    # Insert media_genres
    for genre_id in genre_ids:
        cursor.execute("INSERT IGNORE INTO media_genres (media_id, genre_id) VALUES (%s, %s)", (media["id"], genre_id))
    conn.commit()

    cursor.close()
    conn.close()