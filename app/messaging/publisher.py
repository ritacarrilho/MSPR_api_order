import pika
import aio_pika
import json
import logging
import uuid
import os
from .config import get_rabbitmq_connection

from dotenv import load_dotenv

load_dotenv()

BROKER_USER = os.getenv("BROKER_USER")
BROKER_PASSWORD = os.getenv('BROKER_PASSWORD')
BROKER_HOST = os.getenv('BROKER_HOST')
BROKER_PORT = os.getenv('BROKER_PORT')
BROKER_VIRTUAL_HOST = os.getenv('BROKER_VIRTUAL_HOST')

def publish_message(ch, properties, response_data):
    """Publishes a response back to the producer via RabbitMQ."""
    try:
        response_json = json.dumps(response_data)
        logging.info(f"Publishing response: {response_json}")

        ch.basic_publish(
            exchange='',
            routing_key=properties.reply_to,
            properties=pika.BasicProperties(correlation_id=properties.correlation_id),
            body=response_json
        )

        logging.info(f"Response published successfully for correlation_id: {properties.correlation_id}")
    except Exception as e:
        logging.error(f"Error publishing message: {e}")


def send_rabbitmq_message(queue, message):
    """Send a message to a RabbitMQ queue and wait for a response."""
    try:
        connection = get_rabbitmq_connection()
        if not connection:
            raise Exception("Unable to connect to RabbitMQ.")

        channel = connection.channel()

        channel.queue_declare(queue=queue)

        callback_queue = channel.queue_declare(queue='', exclusive=True).method.queue
        correlation_id = str(uuid.uuid4())
        response = None

        def on_response(ch, method, props, body):
            nonlocal response
            if correlation_id == props.correlation_id:
                response = json.loads(body)

        channel.basic_consume(queue=callback_queue, on_message_callback=on_response, auto_ack=True)

        logging.info(f"Sending message to {queue}: {message}")
        channel.basic_publish(
            exchange='',
            routing_key=queue,
            properties=pika.BasicProperties(
                reply_to=callback_queue,
                correlation_id=correlation_id,
            ),
            body=json.dumps(message)
        )

        while response is None:
            connection.process_data_events()

        connection.close()
        logging.info(f"Received response: {response}")
        return response

    except Exception as e:
        logging.error(f"Error sending message to {queue}: {e}")
        return {"error": str(e)}
    

async def publish_order_created(order):
    connection = await aio_pika.connect_robust(f"amqp://{BROKER_USER}:{BROKER_PASSWORD}@{BROKER_HOST}/")
    async with connection:
        channel = await connection.channel()
        exchange = channel.default_exchange
        
        message = aio_pika.Message(
            body=json.dumps(order).encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )
        
        await exchange.publish(message, routing_key='orders.created')