from fastapi import APIRouter, HTTPException, BackgroundTasks
from .kafka_producer import send_order_event
from .models import Order

router = APIRouter()

# Endpoint to create a new order
@router.post("/orders/")
async def create_order(order: Order, background_tasks: BackgroundTasks):
    order_data = order.dict()  # Convert order object to a dictionary
    background_tasks.add_task(send_order_event, order_data)  # Send the order event in the background
    return {"status": "Order created", "order": order_data}

# Example of fetching order details
@router.get("/orders/{order_id}")
async def get_order(order_id: int):
    # Here, add your database retrieval code
    order = {"id": order_id, "item": "Sample Item", "price": 100}  # Placeholder data
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
