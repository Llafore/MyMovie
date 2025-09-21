import os

from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

class MediaDAO:
    def __init__(self):
        url : str = os.getenv("SUPABASE_URL")
        key : str = os.getenv("SUPABASE_KEY")
        self.supabase: Client = create_client(url, key)

    def load_all_media(self) -> list[dict]:
        return self.supabase.table('media').select('*').execute()

    def insert_media(self, medias: list[dict]):
        self.supabase.table('media').upsert(medias).execute()

    def insert_media_genres(self, medias_genres: list[dict]):
        self.supabase.table('media_genre').upsert(medias_genres).execute()