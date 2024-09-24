import logging
import time
import json
import pika
from .config import get_rabbitmq_connection
from .consumer import on_request
from .service import fetch_order_products
from ..database import get_db
from .publisher import publish_message

def start_order_service_listener():
    """Starts a RabbitMQ listener to handle incoming requests."""
    while True:
        connection = get_rabbitmq_connection()
        if connection:
            try:
                channel = connection.channel()
                channel.queue_declare(queue='customer.orders.request', durable=True)
                channel.queue_declare(queue='order.products.request', durable=True)

                channel.basic_consume(queue='customer.orders.request', on_message_callback=on_request)
                channel.basic_consume(queue='order.products.request', on_message_callback=handle_order_request)

                logging.info("Order Service: RabbitMQ Listener started, waiting for messages.")
                channel.start_consuming()
            except Exception as e:
                logging.error(f"Error in RabbitMQ listener: {e}")
                connection.close()
        else:
            logging.error("RabbitMQ is not available. Retrying in 10 seconds...")
            time.sleep(10)



def handle_order_request(ch, method, properties, body):
    """Handle incoming requests for order products."""
    db = next(get_db()) 
    try:
        data = json.loads(body)
        order_id = data.get('order_id')
        
        order_products = fetch_order_products(db, order_id)
        if not order_products:
            response_data = json.dumps({'error': 'No products found for this order'})
        else:
            product_ids = [op.productId for op in order_products]
            response_data = json.dumps({'products': product_ids})

        ch.basic_publish(
            exchange='',
            routing_key=properties.reply_to, 
            properties=pika.BasicProperties(
                correlation_id=properties.correlation_id
            ),
            body=response_data
        )
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logging.error(f"Error processing order request: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag)
    finally:
        db.close()