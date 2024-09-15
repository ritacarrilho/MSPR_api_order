import aio_pika
import json
import uuid
import asyncio
from aio_pika import Message, IncomingMessage
from ..models import Order
from ..schemas import CustomerOrdersResponse, CustomerOrder
from ..broker.config import get_rabbitmq_connection
from ..database import get_db

# Function to fetch orders from the database (used as fallback or part of microservice logic)
def fetch_orders_from_db(db, customer_id: int):
    orders = db.query(Order).filter(Order.customerId == customer_id).all()
    return [
        CustomerOrder(
            id_order=order.id_order,
            customerId=order.customerId,
            createdAt=order.createdAt,
            updated_at=order.updated_at,
            status=order.status
        ) for order in orders
    ]

async def consume_order_responses():
    connection = await get_rabbitmq_connection()
    async with connection:
        channel = await connection.channel()
        
        # Declare the queue the service listens to
        queue = await channel.declare_queue('order_queue_test', durable=True)

        async def on_request(message: aio_pika.IncomingMessage):
            async with message.process():  # This automatically acknowledges the message unless an exception occurs
                try:
                    # Parse the incoming message to get the customer_id
                    customer_data = json.loads(message.body)
                    customer_id = customer_data.get('customer_id')
                    print(f"Received order request for customer_id: {customer_id}")

                    # Fetch orders from the database
                    db = next(get_db())  # Get a new database session
                    orders = fetch_orders_from_db(db, customer_id)

                    # Prepare the response using the schema
                    response_data = CustomerOrdersResponse(customer_id=customer_id, orders=orders)
                    response_json = response_data.json()

                    # Publish the response back to the 'reply_to' queue specified in the message
                    await message.channel.default_exchange.publish(
                        aio_pika.Message(
                            body=response_json.encode(),
                            correlation_id=message.correlation_id  # Pass the same correlation_id
                        ),
                        routing_key=message.reply_to  # Use the reply_to property to send the response back
                    )
                    print(f"Sent response for customer_id: {customer_id}")

                except Exception as e:
                    print(f"Error processing message: {e}")
                    # You don't need to call nack() or ack() here since `message.process()` handles it.

        print(" [x] Awaiting order requests")
        await queue.consume(on_request)