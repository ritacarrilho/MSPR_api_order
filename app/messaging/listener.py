import logging
import time
from .config import get_rabbitmq_connection
from .consumer import on_request

def start_order_service_listener():
    """Starts a RabbitMQ listener to handle incoming requests."""
    while True:
        connection = get_rabbitmq_connection()
        if connection:
            try:
                channel = connection.channel()
                channel.queue_declare(queue='customer.orders.request', durable=True)

                channel.basic_consume(queue='customer.orders.request', on_message_callback=on_request)
                logging.info("Order Service: RabbitMQ Listener started, waiting for messages.")
                channel.start_consuming()
            except Exception as e:
                logging.error(f"Error in RabbitMQ listener: {e}")
                connection.close()
        else:
            logging.error("RabbitMQ is not available. Retrying in 10 seconds...")
            time.sleep(10)