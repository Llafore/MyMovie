import os
from dao.user_dao import UserDAO
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from models.user import User, UserExistsResponse, UserExistsRequest, UserResponse, UserCreate, UserDelete, UserDeleteResponse, DeleteError
from clerk_backend_api import Clerk
from clerk_backend_api.models.clerkerrors import ClerkErrors


router = APIRouter(
    prefix='/user',
    tags=['users'],
)

clerk = Clerk(
    bearer_auth=os.getenv("CLERK_SECRET_KEY")
)

dao = UserDAO()
security = HTTPBearer()

def get_bearer_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    return credentials.credentials

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

    res = clerk.users.update(
        user_id=user.clerk_id,
        public_metadata={ "username": user.name }
    )
    assert res is not None

    new_user = User(clerk_id=user.clerk_id,
                    name=user.name,
                    email=user.email)

    dao.create_user(new_user)
    return new_user

@router.delete('/delete', response_model=UserDeleteResponse)
async def delete_user(deleteBody: UserDelete, token: str = Depends(get_bearer_token)):
    try:
        print(token)
        dao.delete_user(deleteBody.clerk_id)

        res = clerk.users.delete(user_id=deleteBody.clerk_id, retries=3)
        print(res)
        assert res is not None

        return UserDeleteResponse(detail="deleted succesfully.")

    except ClerkErrors as ce:
        print(f"Clerk error deleting user: {ce}")
        raise HTTPException(status_code=500, detail=f"Clerk error deleting user: {ce.data.errors[0].message}")

    except AssertionError:
        raise HTTPException(status_code=404, detail="User not found in Clerk.")

    except Exception as e:
        print(type(e))
        print(f"Error deleting user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting user: {str(e)}")   
