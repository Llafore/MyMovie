from backend.utils.genre_util import GenreUtil


class MediaUtil:
    @staticmethod
    def normalize_media_genres(medias: list[dict]):
        genre_util = GenreUtil()

        for media in medias:
            media.update({'media_genres_normalized': ''})
            for media_genre in media['media_genres']:
                media['media_genres_normalized'] += genre_util.get_genre_name(media_genre)