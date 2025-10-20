import os

from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

class GenreDAO:
    def __init__(self):
        url : str = os.getenv("SUPABASE_URL")
        key : str = os.getenv("SUPABASE_KEY")
        self.supabase: Client = create_client(url, key)

    def clear_genres(self):
        self.supabase.table('genre').delete().neq("id", 0).execute()

    def insert_genres(self, genres: list[dict]):
        self.supabase.table('genre').upsert(genres).execute()

    def get_all_genres(self) -> list[dict]:
        return (
            self.supabase.
            table('genre')
            .select('*')
            .execute()
            .data
        )