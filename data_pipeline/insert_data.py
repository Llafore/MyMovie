from db_connection import get_connection

def insert_movie_genre(movie):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        INSERT INTO movie_genre (movie_id, genre_id)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE 
          movie_id = VALUES(movie_id),
          genre_id = VALUES(genre_id);
    """

    for genre_id in movie["genre_ids"]:
        values = (movie["id"], genre_id)
        cursor.execute(sql, values)

    conn.commit()
    cursor.close()
    conn.close()


def insert_movie(movie):
    conn = get_connection()
    cursor = conn.cursor()
    release_date = movie["release_date"]

    if not release_date or release_date.strip() == "":
        release_date = None

    sql = (
        "INSERT INTO movies (id, title, description, release_date, poster_path, backdrop_path) "
        "VALUES (%s, %s, %s, %s, %s, %s) "
        "ON DUPLICATE KEY UPDATE "
        "title = VALUES(title), "
        "description = VALUES(description), "
        "release_date = VALUES(release_date), "
        "poster_path = VALUES(poster_path), "
        "backdrop_path = VALUES(backdrop_path)"
    )

    values = (
        movie["id"],
        movie["title"],
        movie["description"],
        release_date,
        movie["poster_path"],
        movie["backdrop_path"]
    )

    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()
    insert_movie_genre(movie)


def insert_genre(genre):
    conn = get_connection()
    cursor = conn.cursor()

    sql = (
        "INSERT INTO genre (id, name) "
        "VALUES (%s, %s) "
        "ON DUPLICATE KEY UPDATE "
        "id = VALUES(id), "
        "name = VALUES(name)"
    )

    values = (genre["id"], genre["name"])

    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()