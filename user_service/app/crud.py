from sqlmodel import Session, select
from fastapi import HTTPException, Depends
from passlib.context import CryptContext
from .models import UserCreate, UserUpdate, ChangePassword, User
from .db import get_session

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Create User
def create_user(user: User, session: Session = Depends(get_session)):  # Changed from 'Users' to 'User'
    statement = select(User).where(User.email == user.email)
    existing_user = session.exec(statement).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)
    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        user_type=1
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

# Get User by ID
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Update User
def update_user(user_id: int, user_update: UserUpdate, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_update.name:
        user.name = user_update.name
    if user_update.email:
        statement = select(User).where(User.email == user_update.email)
        existing_user = session.exec(statement).first()
        if existing_user and existing_user.id != user.id:
            raise HTTPException(status_code=400, detail="Email already in use")
        user.email = user_update.email

    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# Change Password
def change_password(user_id: int, password_data: ChangePassword, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password = hash_password(password_data.password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user 

# Delete User
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    session.delete(user)
    session.commit()
    return {"message": "User deleted successfully"}
