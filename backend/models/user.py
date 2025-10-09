from pydantic import BaseModel

class UserCreate(BaseModel):
    clerk_id: str
    name: str
    email: str
    password: str

class UserResponse(BaseModel):
    clerk_id: str
    name: str
    email: str

class UserExistsRequest(BaseModel):
    id: str

class UserExistsResponse(BaseModel):
    exists: bool

class User:
    def __init__(self, clerk_id, name, email, password, user_id = 0):
        self.clerk_id = clerk_id
        self.name = name
        self.email = email
        self.password = password