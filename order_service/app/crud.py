from app.kafka_producer import send_order_event

@router.post("/", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
async def create_order_endpoint(order: OrderCreate):
    new_order = create_order(order)
    if not new_order:
        raise HTTPException(status_code=400, detail="Order could not be created")
    
    # Publish event to Kafka
    send_order_event("ORDER_CREATED", new_order.dict())
    
    return new_order
