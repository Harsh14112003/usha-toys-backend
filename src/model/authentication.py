from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool = False
    role: str = "user"
    dateCreated: Optional[datetime] = None
    dateModified: Optional[datetime] = None
    is_verified: bool = False
    

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user: User


class TokenData(BaseModel):
    username: str | None = None



    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


class UserCreate(User):
    password: str


class TokenRefresh(BaseModel):
    refresh_token: str