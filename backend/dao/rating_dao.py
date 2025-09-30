import os
from supabase import create_client, Client


class RatingDAO:
    def __init__(self):
        url : str = os.getenv("SUPABASE_URL")
        key : str = os.getenv("SUPABASE_KEY")
        self.supabase: Client = create_client(url, key)

    def get_rating_by_clerk(self, clerk_id: int):
        return (self.supabase
                .table('rating').
                select('media_id, score')
                .eq('clerk_id', clerk_id)
                .execute()
                .data
                )

    def insert_rating(self, media_id: int, clerk_id: int, score: float):
        self.supabase.table('rating').insert({
            'media_id': media_id,
            'clerk_id': clerk_id,
            'score': score
        }).execute()

if __name__ == '__main__':
   dao = RatingDAO()
   print(dao.get_rating_by_clerk(1))