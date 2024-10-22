from typing import Optional
from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field()
    email: str = Field()
    password: str = Field()

class UserCreate(SQLModel):
    name: str = Field()
    email: str = Field()
    password: str = Field()

class UserUpdate(SQLModel):
    name: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None)

class ChangePassword(SQLModel):
    password: str = Field()

class Usertoken(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field()
    email: str = Field()
    user_type: int = Field()

class TokenResponse(SQLModel):
    access_token: str
    token_type: str
