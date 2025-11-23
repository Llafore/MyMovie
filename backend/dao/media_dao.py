from datetime import date 
import os
from typing import List, Optional

from dotenv import load_dotenv
from sqlalchemy.sql.expression import and_, or_
from supabase import create_client, Client
from sqlmodel import Field, Relationship, SQLModel, Session, select
from sqlalchemy.orm import selectinload

import time

from models.media import SearchQuery

load_dotenv()
class MediaGenreLink(SQLModel, table=True):
    __tablename__ = "media_genres"
    id: Optional[int] = Field(default=None, primary_key=True)
    media_id: str = Field(foreign_key="media.id")
    genre_id: int = Field(foreign_key="genre.id")


class Genre(SQLModel, table=True):
    __tablename__ = "genre"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    media: List["Media"] = Relationship(back_populates="genres", link_model=MediaGenreLink)


class People(SQLModel, table=True):
    __tablename__ = "people"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = None
    profile_path: Optional[str] = None


class MediaCreditLink(SQLModel, table=True):
    __tablename__ = "media_credits"
    id: Optional[int] = Field(default=None, primary_key=True)
    media_id: str = Field(foreign_key="media.id")
    people_id: int = Field(foreign_key="people.id")
    character: Optional[str] = None
    name: Optional[str] = None
    role: Optional[str] = None

    person: People = Relationship()
    media: "Media" = Relationship(back_populates="credits")


class Media(SQLModel, table=True):
    __tablename__ = "media"
    id: str = Field(primary_key=True)
    title: Optional[str]
    description: Optional[str]
    release_date: Optional[date]
    poster_path: Optional[str]
    backdrop_path: Optional[str]
    is_movie: Optional[bool] = True

    genres: List[Genre] = Relationship(back_populates="media", link_model=MediaGenreLink)
    credits: List[MediaCreditLink] = Relationship(back_populates="media")

class MediaDAO:
    def __init__(self):

        # self.engine = engine
        
        url : str = os.getenv("SUPABASE_URL")
        key : str = os.getenv("SUPABASE_KEY")
        self.supabase: Client = create_client(url, key)

    def build_where(self, filters):
        conditions = []

        for f in filters:
            col = None

            if f.field == "generic":
                pattern = f"%{f.value}%"
                or_block = [
                    Media.title.ilike(pattern),
                    People.name.ilike(pattern),
                    MediaCreditLink.character.ilike(pattern)
                ]
                conditions.append(or_(*or_block))
                continue

            if f.field == "genre.name":
                col = Genre.name
            elif f.field == "people.name":
                col = People.name
            elif f.field == "people.character":
                col = MediaCreditLink.character
            # Campos diretos
            elif '.' not in f.field:
                try:
                    col = getattr(Media, f.field)
                except AttributeError:
                    continue
            else:
                continue

            if col is None:
                continue

            op = f.operator
            match op:
                case "eq":
                    conditions.append(col == f.value)
                case "neq":
                    conditions.append(col != f.value)
                case "gt":
                    conditions.append(col > f.value)
                case "gte":
                    conditions.append(col >= f.value)
                case "lt":
                    conditions.append(col < f.value)
                case "lte":
                    conditions.append(col <= f.value)
                case "like":
                    conditions.append(col.ilike(f"%{f.value}%"))
                case "in":
                    conditions.append(col.in_(f.value))

        return and_(*conditions) if conditions else None

    def load_media_with_genres(self) -> List[Media]:
        with Session(self.engine) as session:
            statement = select(Media).options(selectinload(Media.genres))
            media_list = session.exec(statement).all()
            return media_list
            
    def load_all_media_banco(self) -> List[Media]:
        with Session(self.engine) as session:
            statement = select(Media)
            media_list = session.exec(statement).all()
            return media_list

    def load_by_query(self, query: SearchQuery):
        with Session(self.engine) as session:
            statement = select(Media).options(
                selectinload(Media.genres),
                selectinload(Media.credits).selectinload(MediaCreditLink.person)
            )

            # 🔹 JOINs opcionais (dependendo dos filtros)
            if query.filters:
                if any(f.field.startswith("genre.") for f in query.filters):
                    statement = statement.join(MediaGenreLink).join(Genre)

                if any(f.field.startswith("people.") or f.field == "generic" for f in query.filters):
                    statement = statement.join(MediaCreditLink).join(People)

                # 🔹 WHERE
                condition = self.build_where(query.filters)
                if condition is not None:
                    statement = statement.where(condition)

            # 🔹 <== INSIRA AQUI o bloco de ordenação e paginação
            if query.sort_by:
                sort_col = getattr(Media, query.sort_by, None)
                if sort_col is not None:
                    if query.sort_order == "desc":
                        statement = statement.order_by(sort_col.desc())
                    else:
                        statement = statement.order_by(sort_col.asc())

            if query.limit:
                statement = statement.limit(query.limit)

            if query.offset:
                statement = statement.offset(query.offset)

            # 🔹 DISTINCT e execução
            statement = statement.distinct()
            results = session.exec(statement).all()
            return results

    def load_by_query_sdk(self, query: SearchQuery):
        params = {
            "search_term": None,
            "genre_filters": None,
            "is_movie_filter": None,
            "clerk_id_param": query.clerk_id
        }
        
        genre_values = []
        
        for f in query.filters or []:
            if f.field == "generic":
                params["search_term"] = f.value
            elif f.field == "genre.name":
                genre_values.append(f.value)
            elif f.field == "is_movie":
                params["is_movie_filter"] = f.value.lower() == "true"
        
        if genre_values:
            params["genre_filters"] = genre_values
        
        sb = self.supabase.rpc("search_query", params)
        
        # Apply sorting and pagination
        if query.sort_by:
            sb = sb.order(query.sort_by, desc=query.sort_order == "desc")
        
        if query.limit:
            start = query.offset or 0
            end = start + query.limit - 1
            sb = sb.range(start, end)
        
        response = sb.execute()
        return response.data

    def load_all_media(self) -> list[dict]:
        return self.supabase.table('media').select('*').execute().data

    def load_media_paginated(self, clerk_id, from_index, to_index) -> list[dict]:
        return (
            self.supabase
            .table('media')
            .select('*, media_credits(*), media_genres(*), watch_later(*)')
            .range(from_index, to_index)
            .filter('watch_later.clerk_id', 'eq', clerk_id)
            .execute()
            .data
        )   

    def load_media_to_df_content(self, batch_size=1000):
        all_medias = []
        start = 0

        while True:
            resp = (
                self.supabase
                .table('media')
                .select('*')
                .range(start, start + batch_size - 1)
                .execute()
            )
            data = resp.data or []
            all_medias.extend(data)

            print(f"Fetched {len(data)} media (total {len(all_medias)})")

            if len(data) < batch_size:
                break

            start += batch_size

        genres = self.supabase.table('media_genres').select('*').execute().data or []
        credits = self.supabase.table('media_credits').select('*').execute().data or []

        from collections import defaultdict
        genres_by_media = defaultdict(list)
        for g in genres:
            genres_by_media[g['media_id']].append(g)

        credits_by_media = defaultdict(list)
        for c in credits:
            credits_by_media[c['media_id']].append(c)

        for m in all_medias:
            m['media_genres'] = genres_by_media[m['id']]
            m['media_credits'] = credits_by_media[m['id']]

        print(f"✅ Finished merging {len(all_medias)} media")
        return all_medias

    def clear_media(self):
        self.supabase.table('media').delete().neq("id", "0").execute()

    def insert_media(self, medias: list[dict]):
        self.supabase.table('media').upsert(medias).execute()

    def clear_media_genres(self):
        self.supabase.table('media_genres').delete().neq("id", 0).execute()

    def insert_media_genres(self, medias_genres: list[dict]):
        self.supabase.table('media_genres').upsert(medias_genres).execute()

    def insert_rating_by_batch(self, clerk_id: str, ratings: list):
        data = [
            {"clerk_id": clerk_id, "media_id": r.media_id, "score": r.score}
            for r in ratings
        ]
        self.supabase.table("rating").upsert(data, on_conflict="clerk_id, media_id").execute()

    def get_medias(self, medias_ids: list[str], clerk_id: str, with_ratings: bool = False, with_bookmarks: bool = False):
        select_query = '*, media_credits(*), media_genres(*)'
        
        if with_ratings:
            select_query += ', rating(*)'
        if with_bookmarks:
            select_query += ', watch_later(*)'

        query = (
            self.supabase
            .table('media')
            .select(select_query)
            .in_('id', medias_ids)
        )

        if with_ratings:
            query = query.filter('rating.clerk_id', 'eq', clerk_id)

        if with_bookmarks:
            query = query.filter('watch_later.clerk_id', 'eq', clerk_id)

        return query.execute().data

    def get_ratings_by_clerk_id(self, clerk_id):
        return (self.supabase
                .table('rating')
                .select('*')
                .eq('clerk_id', clerk_id)
                .execute()
                .data)

    def delete_rating(self, clerk_id, media_id):
        (self.supabase
         .table('rating')
         .delete()
         .eq('clerk_id', clerk_id)
         .eq('media_id', media_id)
         .execute())

    def get_credits_from_medias(self, medias_ids: list[str]):
        return (self.supabase
                .table('media_credits')
                .select('*')
                .in_('media_id', medias_ids)
                .execute()
                .data)

    def get_credits_from_medias(self, medias: list[str]):
        return (self.supabase
                .table('media_credits')
                .select('*, people(profile_path)')
                .in_('media_id', medias)
                .execute()
                .data)

    def get_genres_from_medias(self, medias_ids: list[str]):
        return (self.supabase
                .table('media_genres')
                .select('media_id, genre(name)')
                .in_('media_id', medias_ids)
                .execute()
                .data)

    def load_series_ids(self) -> list[str]:
        return (self.supabase
                .table('media')
                .select('id')
                .eq('is_movie', False)
                .execute()
                .data)

    def load_movies_ids(self) -> list[str]:
        return (self.supabase
                .table('media')
                .select('id')
                .eq('is_movie', True)
                .execute()
                .data)

    def insert_watch_later_by_batch(self, clerk_id, medias):
        data = [
            {"clerk_id": clerk_id, "media_id": media}
            for media in medias
        ]
        self.supabase.table('watch_later').upsert(data).execute()

    def get_watch_later_by_clerk_id(self, clerk_id, page_number: 1, page_size: 10):
        start = (page_number - 1) * page_size
        end = page_number * page_size - 1
        return (self.supabase
                .table('watch_later')
                .select('media_id')
                .eq('clerk_id', clerk_id)
                .order('id', desc=True)
                .range(start, end)
                .execute()
                .data)

    def delete_watch_later(self, clerk_id, media_id):
        (self.supabase
         .table('watch_later')
         .delete()
         .eq('clerk_id', clerk_id)
         .eq('media_id', media_id)
         .execute())


if __name__ == '__main__':
    dao = MediaDAO()

    ts = time.perf_counter()
    data = dao.load_media_to_df_content()
    te = time.perf_counter()
    print(f'Tempo de carga de mídia: {te - ts:0.4f}')

    ts = time.perf_counter()
    data_banco = dao.load_media_with_genres()
    te = time.perf_counter()
    print(f'Tempo de carga de mídia do banco: {te - ts:0.4f}')
    print(len(data))
    print(len(data_banco))
