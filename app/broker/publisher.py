import aio_pika
import pika
import json
import uuid
from sqlalchemy.orm import Session
from ..controllers import fetch_orders_for_customer
from .config import get_rabbitmq_connection
from ..database import get_db


# Function to send a message to the RabbitMQ queue
async def publish_order_request(customer_id: int):
    try:
        # Connect to RabbitMQ
        connection = await aio_pika.connect_robust("amqp://user:password@rabbitmq/")
        channel = await connection.channel()

        # Declare a temporary queue for the response
        result_queue = await channel.declare_queue('', exclusive=True)
        callback_queue = result_queue.name

        # Generate a correlation ID for the request
        corr_id = str(uuid.uuid4())

        # Prepare the message
        message = aio_pika.Message(
            body=json.dumps({'customer_id': customer_id}).encode(),
            reply_to=callback_queue,
            correlation_id=corr_id,
        )

        # Publish the message to the 'order_queue_test'
        await channel.default_exchange.publish(
            message,
            routing_key='order_queue_test'
        )
        print(f"Request sent for customer_id: {customer_id}")

        # Listen for the response on the callback queue
        async with result_queue.iterator() as queue_iter:
            async for response_message in queue_iter:
                if response_message.correlation_id == corr_id:
                    print("Received the correct response")
                    orders = json.loads(response_message.body)
                    return orders['orders']

    except Exception as e:
        print(f"Error publishing message: {e}")

    finally:
        if connection and not connection.is_closed:
            await connection.close()
            print("RabbitMQ connection closed.")

# def publish_order_created(order):
#     """
#     Publish a message when a new order is created.
#     """
#     order_message = {
#         "order_id": order.id_order,
#         "customer_id": order.customerId,
#         "status": order.status,
#         "products": [
#             {"product_id": op.productId, "quantity": op.quantity} for op in order.order_products
#         ],
#         "created_at": str(order.createdAt),
#     }
#     publish_message('order_exchange', 'order.created', order_message)


# def publish_order_updated(order):
#     """
#     Publish a message when an order is updated.
#     """
#     order_message = {
#         "order_id": order.id_order,
#         "customer_id": order.customerId,
#         "status": order.status,
#         "products": [
#             {"product_id": op.productId, "quantity": op.quantity} for op in order.order_products
#         ],
#         "updated_at": str(order.updated_at),
#     }
#     publish_message('order_exchange', 'order.updated', order_message)


# def publish_order_deleted(order_id):
#     """
#     Publish a message when an order is deleted.
#     """
#     order_message = {
#         "order_id": order_id
#     }
#     publish_message('order_exchange', 'order.deleted', order_message)








def on_request(ch, method, props, body, db_session: Session):
    # Parse the request data
    customer_data = json.loads(body)
    customer_id = customer_data.get("customer_id")
    
    print(f"Received request for customer_id: {customer_id}")

    # Fetch orders from the database using the controller function
    try:
        response_data = fetch_orders_for_customer(db_session, customer_id)

        if response_data is None:
            response_json = json.dumps({"error": "No orders found for this customer"})
            # Send the error response back via RabbitMQ
            ch.basic_publish(
                exchange='',
                routing_key=props.reply_to,
                properties=pika.BasicProperties(correlation_id=props.correlation_id),
                body=response_json
            )
        else:
            # Convert the response data to JSON and send it back
            response_json = response_data.json()
            ch.basic_publish(
                exchange='',
                routing_key=props.reply_to,
                properties=pika.BasicProperties(correlation_id=props.correlation_id),
                body=response_json
            )
        
        print(f"Response sent for customer_id: {customer_id}")
        
    except Exception as e:
        print(f"An error occurred while processing the request for customer_id {customer_id}: {e}")
        error_response = json.dumps({"error": "Failed to fetch orders"})
        ch.basic_publish(
            exchange='',
            routing_key=props.reply_to,
            properties=pika.BasicProperties(correlation_id=props.correlation_id),
            body=error_response
        )

    # Acknowledge the message to RabbitMQ
    ch.basic_ack(delivery_tag=method.delivery_tag)

# RabbitMQ listener setup
def start_order_service_listener():
    connection = get_rabbitmq_connection()  # Assumes there's a function to get the RabbitMQ connection
    channel = connection.channel()

    # Declare the queue if necessary
    channel.queue_declare(queue='order_queue_test', durable=True)

    # Start consuming messages from RabbitMQ
    def callback(ch, method, props, body):
        # Set up a new session for each request
        db_session = next(get_db())  # Assuming get_db() is the function for getting a database session
        on_request(ch, method, props, body, db_session)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='order_queue_test', on_message_callback=callback)

    print(" [x] Awaiting RPC requests")
    channel.start_consuming()



def publish_message():
    """
    Publish a message to RabbitMQ.
    """
    try:
        # Connection parameters
        credentials = pika.PlainCredentials('user', 'password')
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', port=5672, virtual_host='/', credentials=credentials))
        channel = connection.channel()

        channel.queue_declare(queue='order_queue_test', durable=True)
        # Declare an exchange
        channel.exchange_declare(exchange='order_queue_exchange', exchange_type='direct')

        # Publish a message
        message = "Hello from Service A!"
        channel.basic_publish(exchange='order_queue_exchange', routing_key='order_queue_test', body=message)

        channel.basic_publish(
            exchange='',
            routing_key='order_queue_test',
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent
            ))

        print(f" [x] Sent '{message}'")

        # Close the connection
        connection.close()

    except Exception as e:
        print(f"Error publishing message: {e}")
