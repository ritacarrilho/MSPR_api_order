from ..models import Order
from ..schemas import CustomerOrdersResponse, CustomerOrder

# Function to fetch orders from the database
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