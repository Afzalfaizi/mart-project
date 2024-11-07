from app.models import Payment
from app.schemas import PaymentCreate
from sqlmodel import Session
from app.settings import KAFKA_BROKER_URL
from aiokafka import AIOKafkaProducer
import asyncio
import json

# Initialize Kafka producer asynchronously
async def get_kafka_producer():
    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )
    await producer.start()
    return producer

# Send Kafka event asynchronously
async def send_kafka_event(producer, topic, event):
    try:
        await producer.send(topic, event)
    except Exception as e:
        print(f"Failed to send event: {e}")

# Payment creation service
async def create_payment(session: Session, payment_data: PaymentCreate):
    payment = Payment(
        order_id=payment_data.order_id,
        amount=payment_data.amount,
        payment_method=payment_data.payment_method,
        status="Pending"
    )
    session.add(payment)
    session.commit()
    session.refresh(payment)

    producer = await get_kafka_producer()
    await send_kafka_event(producer, "payment_events", {
        "event": "payment_initiated",
        "payment_id": payment.id,
        "status": payment.status
    })
    await producer.stop()
    return payment

# Payment status update service
async def update_payment_status(session: Session, payment_id: int, status: str):
    payment = session.get(Payment, payment_id)
    if payment:
        payment.status = status
        session.commit()

        producer = await get_kafka_producer()
        await send_kafka_event(producer, "payment_events", {
            "event": "payment_status_updated",
            "payment_id": payment_id,
            "status": status
        })
        await producer.stop()
    return payment
