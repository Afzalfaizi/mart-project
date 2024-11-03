from kafka import KafkaProducer
import json
from app.settings import KAFKA_BROKER_URL

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER_URL],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_order_event(event_type: str, order_data: dict):
    """Send order events to Kafka."""
    event = {
        "event_type": event_type,
        "order_data": order_data
    }
    producer.send('order_events', value=event)
    producer.flush()
