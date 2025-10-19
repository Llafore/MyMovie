from pydantic import BaseModel
from clerk_backend_api.models import ClerkError

class UserCreate(BaseModel):
    clerk_id: str
    name: str
    email: str

class UserResponse(BaseModel):
    clerk_id: str
    name: str
    email: str

class UserExistsRequest(BaseModel):
    id: str

class UserExistsResponse(BaseModel):
    exists: bool

class UserDelete(BaseModel):
    clerk_id: str

class UserDeleteResponse(BaseModel):
    detail: str

class User:
    def __init__(self, clerk_id, name, email, user_id = 0):
        self.clerk_id = clerk_id
        self.name = name
        self.email = email

class DeleteError(BaseException):
    clerk_error: ClerkError