from fastapi import FastAPI, Depends, HTTPException, status, Form
from sqlmodel import Session
from app.crud import create_user, get_user, update_user, change_password, delete_user, User
from app.models import UserCreate, UserUpdate, ChangePassword
from app.db import get_session, create_tables
from app.auth import (
    get_password_hash,
    create_access_token,
    authenticate_user,
    get_current_active_user,
)
from fastapi.security import OAuth2PasswordRequestForm  # For OAuth2 form handling
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS (for Swagger UI testing purposes; you may adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create the tables at startup
@app.on_event("startup")
def on_startup():
    create_tables()

@app.get("/")
def read_root():
    return {"message": "Welcome to Mart User Service"}

# Endpoint to obtain JWT token
@app.post("/token")
def login(
    username: str = Form(...), 
    password: str = Form(...), 
    session: Session = Depends(get_session)
):
    user = authenticate_user(username, password, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
# Endpoint for User Registration
@app.post("/register/", response_model=User)
def register_user(user: UserCreate, session: Session = Depends(get_session)):
    user_in_db = User(
        username=user.username,
        full_name=user.full_name,
        email=user.email,
        hashed_password=get_password_hash(user.password)  # Hash the password
    )
    return create_user(user_in_db, session)

# Routes for User operations
@app.post("/add_user/", response_model=User, dependencies=[Depends(get_current_active_user)])  # Protect this route
def create_new_user(user: User, session: Session = Depends(get_session)):
    return create_user(user, session)

@app.get("/get_user/{user_id}", response_model=User)  # Protect this route
def read_user(user_id: int, session: Session = Depends(get_session)):
    return get_user(user_id, session)

@app.put("/update_user/{user_id}", response_model=User, dependencies=[Depends(get_current_active_user)])  # Protect this route
def update_existing_user(user_id: int, user: UserUpdate, session: Session = Depends(get_session)):
    return update_user(user_id, user, session)

@app.put("/update_password/{user_id}/password", response_model=User, dependencies=[Depends(get_current_active_user)])  # Protect this route
def update_user_password(user_id: int, password_data: ChangePassword, session: Session = Depends(get_session)):
    return change_password(user_id, password_data, session)

@app.delete("/delete_user/{user_id}", response_model=dict, dependencies=[Depends(get_current_active_user)])  # Protect this route
def remove_user(user_id: int, session: Session = Depends(get_session)):
    return delete_user(user_id, session)
