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
    media_id: int = Field(foreign_key="media.id")
    genre_id: int = Field(foreign_key="genre.id")


class Genre(SQLModel, table=True):
    __tablename__ = "genre"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    media: List["Media"] = Relationship(back_populates="genres", link_model=MediaGenreLink)


class Media(SQLModel, table=True):
    __tablename__ = "media"
    id: int = Field(primary_key=True)
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

    def load_media_to_df_content(self):
        return (
            self.supabase
            .table('media')
            .select('*, media_genres!inner(*)')
            .execute()
            .data
        )

    def insert_media(self, medias: list[dict]):
        self.supabase.table('media').upsert(medias).execute()

    def insert_media_genres(self, medias_genres: list[dict]):
        self.supabase.table('media_genres').upsert(medias_genres).execute()
    
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
