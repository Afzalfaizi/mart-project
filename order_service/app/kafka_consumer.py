from kafka import KafkaConsumer
import json
from app.settings import KAFKA_BROKER_URL

# Initialize Kafka consumer
consumer = KafkaConsumer(
    'order_events',  # Topic to listen to
    bootstrap_servers=[KAFKA_BROKER_URL],
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    group_id="order_service_consumer"
)

def consume_order_events():
    """Continuously listen for order events from Kafka."""
    for message in consumer:
        event = message.value
        process_order_event(event)

def process_order_event(event):
    """Process order events."""
    event_type = event.get("event_type")
    order_data = event.get("order_data")

    if event_type == "ORDER_CREATED":
        print(f"New order created: {order_data}")
        # Add custom logic here, e.g., notify another service, update inventory, etc.
    elif event_type == "ORDER_UPDATED":
        print(f"Order updated: {order_data}")
        # Additional logic for updating orders
