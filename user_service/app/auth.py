from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlmodel import Session
from .models import User
from .db import get_session
from app.settings import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM

# Set up password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Set up OAuth2 password flow
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Hash a password
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Verify a password against a hashed password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Retrieve a user by email
def get_user_by_email(email: str, session: Session) -> Optional[User]:
    return session.query(User).filter(User.email == email).first()

# Authenticate the user
def authenticate_user(email: str, password: str, session: Session) -> Optional[User]:
    user = get_user_by_email(email, session)
    if user and verify_password(password, user.hashed_password):
        return user
    return None

# Generate a JWT access token
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Retrieve the current user from the token
def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_email(email, session)
    if user is None:
        raise credentials_exception
    return user

# Retrieve the current active user
def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if getattr(current_user, "disabled", False):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
