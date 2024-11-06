from fastapi import FastAPI, BackgroundTasks
from app.crud import router as order_router
from app.kafka_consumer import consume_order_events

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # Run Kafka consumer in background
    background_tasks = BackgroundTasks()
    background_tasks.add_task(consume_order_events)

app.include_router(order_router, prefix="/orders", tags=["orders"])

@app.get("/")
async def root():
    return {"message": "Order Service is up and running"}
