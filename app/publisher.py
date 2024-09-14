import pika
import json

def publish_message(exchange, routing_key, message_body):
    """
    Publish a message to RabbitMQ.
    """
    try:
        # Establish connection to RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))  # RabbitMQ container in Docker
        channel = connection.channel()

        # Declare the exchange (direct exchange)
        channel.exchange_declare(exchange=exchange, exchange_type='direct', durable=True)

        # Publish the message
        channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=json.dumps(message_body),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
            )
        )

        print(f"Message Published: {routing_key}")
        connection.close()

    except Exception as e:
        print(f"Error publishing message: {e}")


def publish_order_created(order):
    """
    Publish a message when a new order is created.
    """
    order_message = {
        "order_id": order.id_order,
        "customer_id": order.customerId,
        "status": order.status,
        "products": [
            {"product_id": op.productId, "quantity": op.quantity} for op in order.order_products
        ],
        "created_at": str(order.createdAt),
    }
    publish_message('order_exchange', 'order.created', order_message)


def publish_order_updated(order):
    """
    Publish a message when an order is updated.
    """
    order_message = {
        "order_id": order.id_order,
        "customer_id": order.customerId,
        "status": order.status,
        "products": [
            {"product_id": op.productId, "quantity": op.quantity} for op in order.order_products
        ],
        "updated_at": str(order.updated_at),
    }
    publish_message('order_exchange', 'order.updated', order_message)


def publish_order_deleted(order_id):
    """
    Publish a message when an order is deleted.
    """
    order_message = {
        "order_id": order_id
    }
    publish_message('order_exchange', 'order.deleted', order_message)