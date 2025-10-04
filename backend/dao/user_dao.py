import os

from dotenv import load_dotenv
from supabase import create_client, Client

from models.user import User

load_dotenv()

class UserDAO:
    def __init__(self):
        url : str = os.getenv("SUPABASE_URL")
        key : str = os.getenv("SUPABASE_KEY")
        self.supabase: Client = create_client(url, key)

    def find_by_email(self, email: str):
        data = (self.supabase
                .table('user')
                .select('*')
                .eq('email', email)
                .execute()
                ).data

        if not data:
            return None

        return User(clerk_id=data[0]['clerk_id'],
                    name=data[0]['name'],
                    email=data[0]['email'],
                    password=data[0]['password']
                    )

    def find_by_id(self, id: str):
        data = (self.supabase
                .table('user')
                .select('*')
                .eq('clerk_id', id)
                .execute()
                ).data

        if not data:
            return None

        return User(clerk_id=data[0]['clerk_id'],
                    name=data[0]['name'],
                    email=data[0]['email'],
                    password=data[0]['password']
                    )

    def create_user(self, user: User):
        if self.find_by_email(user.email):
            return False
        user_dict = {
            'clerk_id': user.clerk_id,
            'email': user.email,
            'name': user.name,
            'password': user.password,
        }
        self.supabase.table('user').insert(user_dict).execute()
        return True