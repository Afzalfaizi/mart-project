from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlmodel import Session
from models import User  # Assuming User is defined in models.py
from database import get_session  # Assuming get_session is your session dependency


# Password hashing and verification context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for token generation and verification
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Function to hash password
def get_password_hash(password: str):
    return pwd_context.hash(password)

# Function to verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Function to retrieve user from the database
def get_user_from_db(email: str, session: Session):
    user = session.query(User).filter(User.email == email).first()
    return user

# Authenticate the user by verifying credentials
def authenticate_user(email: str, password: str, session: Session):
    user = get_user_from_db(email, session)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

# Create access token for the authenticated user
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Get current user based on the JWT token
def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
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

    user = get_user_from_db(email, session)
    if user is None:
        raise credentials_exception
    return user

# Check if the user is active
def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
