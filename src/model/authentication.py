from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool = False
    role: str = "user"
    

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