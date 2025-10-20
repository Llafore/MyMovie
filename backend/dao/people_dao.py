from supabase import create_client, Client
import os

class PeopleDAO:
    def __init__(self):
        url : str = os.getenv("SUPABASE_URL")
        key : str = os.getenv("SUPABASE_KEY")
        self.supabase: Client = create_client(url, key)

    def clear_people(self):
        self.supabase.table('people').delete().neq("id", 0).execute()

    def clear_credits(self):
        self.supabase.table('media_credits').delete().neq("id", 0).execute()

    def insert_people(self, peoples: list[dict]):
        self.supabase.table('people').upsert(peoples).execute()

    def insert_credits(self, credits):
        self.supabase.table('media_credits').upsert(credits).execute()
