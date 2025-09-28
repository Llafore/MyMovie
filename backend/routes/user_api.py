from backend.dao.user_dao import UserDAO
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.models.user import User


class UserCreate(BaseModel):
    id: int
    name: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

router = APIRouter(
    prefix='/user',
    tags=['users'],
)

dao = UserDAO()

@router.post('/new_user', response_model=UserResponse)
def create_user(user: UserCreate):
    new_user = User(name=user.name, email=user.email, password=user.password, user_id=user.id)
    dao.create_user(new_user)
    return new_user