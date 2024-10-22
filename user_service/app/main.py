from fastapi import FastAPI, Depends
from sqlmodel import Session
from .crud import create_user, get_user, update_user, change_password, delete_user, User
from .models import UserCreate, UserUpdate, ChangePassword
from .db import get_session, create_tables

app = FastAPI()

# Create the tables at startup
@app.on_event("startup")
def on_startup():
    create_tables()
    
@app.get("/")
def  read_root():
    return("welcome to mart user service")


# Routes for User operations

@app.post("/add_user/", response_model=User)
def create_new_user(user: UserCreate, session: Session = Depends(get_session)):
    return create_user(user, session)

@app.get("/get_user/{user_id}", response_model=User)
def read_user(user_id: int, session: Session = Depends(get_session)):
    return get_user(user_id, session)

@app.put("/update_user/{user_id}", response_model=User)
def update_existing_user(user_id: int, user: UserUpdate, session: Session = Depends(get_session)):
    return update_user(user_id, user, session)

@app.put("/update_password/{user_id}/password", response_model=User)
def update_user_password(user_id: int, password_data: ChangePassword, session: Session = Depends(get_session)):
    return change_password(user_id, password_data, session)

@app.delete("/delete_user/{user_id}", response_model=dict)
def remove_user(user_id: int, session: Session = Depends(get_session)):
    return delete_user(user_id, session)
