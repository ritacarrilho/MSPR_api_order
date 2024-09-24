from sqlalchemy.orm import Session
from ..models import Order, OrderProduct
from ..schemas import CustomerOrdersResponse, CustomerOrder

def fetch_orders_for_customer(db, customer_id: int):
    """Fetch all orders associated with a given customer ID from the database."""
    try:
        orders = db.query(Order).filter(Order.customerId == customer_id).all()

        if not orders:
            return None

        order_list = [
            CustomerOrder(
                id_order=order.id_order,
                createdAt=order.createdAt,
                updated_at=order.updated_at,
                status=order.status
            )
            for order in orders
        ]

        return CustomerOrdersResponse(customer_id=customer_id, orders=order_list)
    finally:
        db.close()


def fetch_order_products(db: Session, order_id: int):
    """Fetch the products associated with a specific order ID."""
    try:
        order_products = db.query(OrderProduct).filter(OrderProduct.id_order == order_id).all()
        return order_products if order_products else None

    except Exception as e:
        raise Exception(f"Error fetching products for order {order_id}: {str(e)}")
    


