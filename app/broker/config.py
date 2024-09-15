import pika
import json
import time


def get_rabbitmq_connection():
    credentials = pika.PlainCredentials('user', 'password')
    return pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', port=5672, virtual_host='/', credentials=credentials))


def setup_rabbitmq():
    """
    Setup RabbitMQ exchanges, queues, and bindings.
    """
    try:
        connection = get_rabbitmq_connection()
        channel = connection.channel()

        # Declare the order exchange (direct exchange for order-related messages)
        channel.exchange_declare(exchange='order_exchange', exchange_type='direct', durable=True)

        # Declare the order queues
        # channel.queue_declare(queue='order_created_queue', durable=True)
        channel.queue_declare(queue='order_queue_test', durable=True)
        # channel.queue_declare(queue='order_updated_queue', durable=True)
        # channel.queue_declare(queue='order_deleted_queue', durable=True)

        # Bind the order queues to the exchange with respective routing keys
        # channel.queue_bind(exchange='order_exchange', queue='order_created_queue', routing_key='order.created')
        # channel.queue_bind(exchange='order_exchange', queue='order_updated_queue', routing_key='order.updated')
        # channel.queue_bind(exchange='order_exchange', queue='order_deleted_queue', routing_key='order.deleted')

        print("RabbitMQ setup complete with exchanges and queues.")
        connection.close()

    except Exception as e:
        print(f"Error setting up RabbitMQ: {e}")


