import json
import logging
from .service import fetch_orders_for_customer
from .publisher import publish_message
from ..database import get_db

# Function to handle incoming RabbitMQ messages
def on_request(ch, method, properties, body):
    db = next(get_db())
    try:
        if not body or body.strip() == "":
            logging.error("Empty or invalid message body received.")
            ch.basic_nack(delivery_tag=method.delivery_tag)
            return

        customer_data = json.loads(body)
        customer_id = customer_data.get('customer_id')
        logging.info(f"Processing request for customer_id: {customer_id}")

        # Fetch customer orders from database
        response_data = fetch_orders_for_customer(db, customer_id)

        if response_data is None:
            response_json = {"error": "No orders found for this customer"}
        else:
            response_json = response_data.json()

        # Publish the response via RabbitMQ
        publish_message(ch, properties, response_json)

        # Acknowledge the message
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except json.JSONDecodeError as e:
        logging.error(f"JSON decoding error: {e} - Raw body: {body}")
        ch.basic_nack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logging.error(f"Error handling request: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag)
    finally:
        db.close()