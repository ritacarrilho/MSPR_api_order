import json
import aio_pika
import asyncio
from .config import get_rabbitmq_connection  # Import the connection from config
from ..services.order_service import consume_order_responses
from aio_pika import connect_robust

async def on_message(message: aio_pika.IncomingMessage):
    async with message.process():
        try:
            # Parse the message body
            customer_data = json.loads(message.body.decode())
            customer_id = customer_data.get("customer_id")
            print(f"Received request for customer_id: {customer_id}")

            # Call the service layer to process the request
            orders = await consume_order_responses()

            # Prepare the response data
            response_data = json.dumps({"orders": orders})
            response_message = aio_pika.Message(
                body=response_data.encode(),
                correlation_id=message.correlation_id
            )

            # Send the response back via RabbitMQ
            await message.reply(response_message)
            print(f"Response sent for customer_id: {customer_id}")
        
        except Exception as e:
            print(f"Error processing message: {e}")

# RabbitMQ listener setup
async def start_consumer():
    try:
        # Use the connection from the config file
        connection = await get_rabbitmq_connection()
        channel = await connection.channel()

        # Declare the queue
        queue = await channel.declare_queue('order_queue_test', durable=True)

        # Start consuming messages from the queue
        await queue.consume(on_message)

        print(" [x] Awaiting RPC requests")

        # Keep the connection open
        return connection

    except Exception as e:
        print(f"Error starting consumer: {e}")

async def start_consumer():
    connection = await connect_robust("amqp://user:password@rabbitmq/")
    channel = await connection.channel()

    # Declare your queues and other RabbitMQ logic here
    queue = await channel.declare_queue("order_queue_test", durable=True)
    await queue.consume(on_message)

    print(" [x] Waiting for messages. To exit press CTRL+C")

    return connection

async def run_consumer():
    await consume_order_responses()