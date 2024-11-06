import asyncio
from aiokafka import AIOKafkaProducer

async def send_order_event(order_data: dict):
    producer = AIOKafkaProducer(
        bootstrap_servers='localhost:9092'
    )
    await producer.start()
    try:
        await producer.send_and_wait("order_topic", order_data.encode('utf-8'))
    finally:
        await producer.stop()
