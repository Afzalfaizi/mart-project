from typing import Optional
from sqlmodel import Field, SQLModel
from pydantic import BaseModel

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field()  # Ensure this is present
    full_name: str = Field()  # Also ensure this is here
    email: str = Field()
    hashed_password: str = Field()

class UserCreate(BaseModel):
    username: str
    full_name: str
    email: str
    password: str  # Assuming you have a password field
    
class UserUpdate(SQLModel):
    username: Optional[str] = Field(default=None)  # Fixed field name to match User model
    email: Optional[str] = Field(default=None)

class ChangePassword(SQLModel):
    password: str = Field()

class TokenResponse(SQLModel):
    access_token: str
    token_type: str
