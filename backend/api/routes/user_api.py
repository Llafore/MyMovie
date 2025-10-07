from dao.user_dao import UserDAO
from fastapi import APIRouter, HTTPException

from models.user import User, UserExistsResponse, UserExistsRequest, UserResponse, UserCreate

router = APIRouter(
    prefix='/user',
    tags=['users'],
)

dao = UserDAO()

@router.post('/check_user', response_model=UserExistsResponse)
def check_user(request_body: UserExistsRequest):
    user = dao.find_by_id(request_body.id)
    if user:
        return UserExistsResponse(exists=True)
    if not user:
        return UserExistsResponse(exists=False)
    raise HTTPException(status_code=500, detail="Error checking user")

@router.post('/new_user', response_model=UserResponse)
def create_user(user: UserCreate):
    new_user = User(clerk_id=user.clerk_id,
                    name=user.name,
                    email=user.email,
                    password=user.password)
    dao.create_user(new_user)
    return new_user