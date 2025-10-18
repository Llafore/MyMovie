from utils.genre_util import GenreUtil


class MediaUtil:
    @staticmethod
    def normalize_media_genres(medias: list[dict]):
        genre_util = GenreUtil()

        for media in medias:
            media.update({'media_genres_normalized': ''})
            for media_genre in media['media_genres']:
                media['media_genres_normalized'] += genre_util.get_genre_name(media_genre)

    @staticmethod
    def normalize_media_credits(medias: list[dict]):

        for media in medias:
            media.update({'media_credits_normalized': ''})
            for media_credit in media['media_credits']:
                media['media_credits_normalized'] += str(media_credit['people_id']) + ' '