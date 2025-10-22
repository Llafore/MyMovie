from datetime import date 
import os
from typing import List, Optional

from dotenv import load_dotenv
from supabase import create_client, Client
from sqlmodel import Field, Relationship, SQLModel, create_engine, Session, select
from sqlalchemy.orm import selectinload

import time

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
    
class MediaDAO:
    def __init__(self):

        USER = os.getenv("user")
        PASSWORD = os.getenv("password")
        HOST = os.getenv("host")
        PORT = os.getenv("port")
        DBNAME = os.getenv("dbname")

        DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}"

        self.engine = create_engine(DATABASE_URL, echo=False)
        
        url : str = os.getenv("SUPABASE_URL")
        key : str = os.getenv("SUPABASE_KEY")
        self.supabase: Client = create_client(url, key)

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

    def load_all_media(self) -> list[dict]:
        return self.supabase.table('media').select('*').execute().data

    def load_media_paginated(self, from_index, to_index) -> list[dict]:
        return (
            self.supabase
            .table('media')
            .select('*')
            .range(from_index, to_index)
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
        self.supabase.table("rating").insert(data).execute()

    def get_medias(self, medias_ids: list[str]):
        return (self.supabase
                .table('media')
                .select('*')
                .in_('id', medias_ids)
                .execute()
                .data)

    def get_ratings_by_clerk_id(self, clerk_id):
        return (self.supabase
                .table('rating')
                .select('media_id, score')
                .eq('clerk_id', clerk_id)
                .execute()
                .data)

    def get_credits_from_medias(self, medias_ids: list[str]):
        return (self.supabase
                .table('media_credits')
                .select('*')
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
