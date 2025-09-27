from backend.dao.genre_dao import GenreDAO


class GenreUtil:
    def __init__(self):
        dao = GenreDAO()
        self.genres = dao.get_all_genres()

    def get_genre_name(self, media_genre: dict) -> str|None:
        for genre in self.genres:
            if genre['id'] == media_genre['genre_id']:
                return genre['name'] + ' '
        return ' '