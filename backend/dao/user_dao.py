import os

from dotenv import load_dotenv
from supabase import create_client, Client

from backend.models.user import User

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
                ).data[0]

        if not data:
            return None

        return User(name=data['name'], email=data['email'], password=data['password'], user_id=data['id'])

    def create_user(self, user: User):
        if self.find_by_email(user.email):
            return False
        user_dict = {
            'email': user.email,
            'name': user.name,
            'password': user.password,
        }
        self.supabase.table('user').insert(user_dict).execute()
        return True

    def login(self, email: str, password: str):
        user = self.find_by_email(email)
        if user and user.password == password:
            return user
        return None