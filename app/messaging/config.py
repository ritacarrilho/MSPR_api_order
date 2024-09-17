''' 
This module initialize RabbitMQ and define the consumer logic.
'''

import pika
import os
from dotenv import load_dotenv

load_dotenv()

BROKER_USER = os.getenv("BROKER_USER")
BROKER_PASSWORD = os.getenv('BROKER_PASSWORD')
BROKER_HOST = os.getenv('BROKER_HOST')
BROKER_PORT = os.getenv('BROKER_PORT')
BROKER_VIRTUAL_HOST = os.getenv('BROKER_VIRTUAL_HOST')

# RabbitMQ connection configuration
def get_rabbitmq_connection():
    try:
        credentials = pika.PlainCredentials(BROKER_USER, BROKER_PASSWORD)
        return pika.BlockingConnection(
            pika.ConnectionParameters(host=BROKER_HOST, port=BROKER_PORT, virtual_host=BROKER_VIRTUAL_HOST, credentials=credentials)
        )
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Failed to connect to RabbitMQ: {e}")
        raise