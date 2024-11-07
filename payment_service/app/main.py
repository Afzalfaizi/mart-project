from fastapi import FastAPI
from app.routes import router as payment_router
from app.db import init_db

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(payment_router)
