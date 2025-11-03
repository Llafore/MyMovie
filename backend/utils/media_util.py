from dao.media_dao import Media
from models.media import CastDTO, MediaDTO
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

    @staticmethod
    def sql_to_dto(medias_list: list[Media]):
        media_dtos = []
        for media in medias_list:
            genres = [genre.name for genre in media.genres]
            cast = [
                CastDTO(
                    role=credit.role,
                    name=credit.name,
                    character_name=credit.character,
                    profile_path=credit.person.profile_path if credit.person else None
                )
                for credit in media.credits
            ]

            media_dto = MediaDTO(
                id=media.id,
                title=media.title,
                description=media.description,
                release_date=media.release_date,
                poster_path=media.poster_path,
                backdrop_path=media.backdrop_path,
                is_movie=media.is_movie,
                genres=genres,
                cast=cast
            )
            media_dtos.append(media_dto)

        return media_dtos