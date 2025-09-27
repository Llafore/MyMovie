from backend.dao.user_dao import UserDAO
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.models.user import User


class UserCreate(BaseModel):
    name: str = ""
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    id: int
    name: str
    email: str

router = APIRouter(
    prefix='/user',
    tags=['users'],
)

dao = UserDAO()

@router.post('/login', response_model=LoginResponse)
def login_user(credentials: LoginRequest):
    user = dao.login(credentials.email, credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return user


@router.post('/')
def create_user(user: UserCreate):
    new_user = User(name=user.name, email=user.email, password=user.password)
    dao.create_user(new_user)
    return new_user