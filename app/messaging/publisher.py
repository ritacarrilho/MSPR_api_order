import pika
import json
import logging
import uuid
from .config import get_rabbitmq_connection


def publish_message(ch, properties, response_data):
    """Publishes a response back to the producer via RabbitMQ."""
    try:
        # Convert the response data to JSON
        response_json = json.dumps(response_data)
        logging.info(f"Publishing response: {response_json}")

        # Publish the message to the producer
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
        # Establish RabbitMQ connection
        connection = get_rabbitmq_connection()
        if not connection:
            raise Exception("Unable to connect to RabbitMQ.")

        channel = connection.channel()

        # Declare the queue in case it doesn't exist
        channel.queue_declare(queue=queue)

        # Create a temporary callback queue for the response
        callback_queue = channel.queue_declare(queue='', exclusive=True).method.queue
        correlation_id = str(uuid.uuid4())
        response = None

        # Define a callback for handling the response
        def on_response(ch, method, props, body):
            nonlocal response
            if correlation_id == props.correlation_id:
                response = json.loads(body)

        # Start consuming messages from the callback queue
        channel.basic_consume(queue=callback_queue, on_message_callback=on_response, auto_ack=True)

        # Publish the message to the specified queue
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

        # Wait for the response
        while response is None:
            connection.process_data_events()

        # Close the connection
        connection.close()

        logging.info(f"Received response: {response}")
        return response

    except Exception as e:
        logging.error(f"Error sending message to {queue}: {e}")
        return {"error": str(e)}