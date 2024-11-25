from fastapi import FastAPI,Depends,HTTPException
from contextlib import asynccontextmanager
from app.db import connection_string, create_engine, create_tables
from .image_routes import router2
from app.route import router
from .kafka import kafka_consumer
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("lifspan event is started")
    print("table creating....")
    create_tables()
    print("creating table succesfully")
    task = asyncio.create_task(kafka_consumer('product_topic','broker:19092'))
    task2 = asyncio.create_task(kafka_consumer("product_image",'broker:19092'))
    yield
    
    
app = FastAPI(lifespan=lifespan,
               title="FastAPI Service",
               description="This is a FastAPI Service",
               version="0.0.1"
)



@app.get("/")
async def root():
    return {"message": "welcome to the E_Mart product Service"}

app.include_router(router=router)
app.include_router(router=router2)
