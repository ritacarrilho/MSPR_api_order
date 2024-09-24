import unittest
from datetime import datetime
from pydantic import ValidationError
from app.schemas import (  # Remplacez par le nom de votre module contenant les schémas
    OrderCreate,
    Order,
    OrderProductCreate,
    OrderProduct,
    OrderUpdate,
    OrderProductUpdate,
    CustomerOrder,
    CustomerOrdersResponse,
)

class TestOrderSchemas(unittest.TestCase):

    def test_order_create_valid(self):
        order_data = {
            "customerId": 1,
            "status": 1,
            "createdAt": datetime.now(),
            "updated_at": datetime.now()
        }
        order = OrderCreate(**order_data)
        self.assertEqual(order.customerId, 1)
        self.assertEqual(order.status, 1)

    def test_order_invalid_customer_id(self):
        with self.assertRaises(ValidationError):
            OrderCreate(customerId="invalid", status=1, createdAt=datetime.now(), updated_at=datetime.now())

    def test_order_product_create_valid(self):
        order_product_data = {
            "productId": 1,
            "quantity": 5,
            "id_order": 1
        }
        order_product = OrderProductCreate(**order_product_data)
        self.assertEqual(order_product.productId, 1)
        self.assertEqual(order_product.quantity, 5)

    def test_order_product_invalid_quantity(self):
        with self.assertRaises(ValidationError):
            OrderProductCreate(productId=1, quantity="invalid", id_order=1)

    def test_order_update_valid(self):
        order_update_data = {
            "customerId": 1,
            "status": 2
        }
        order_update = OrderUpdate(**order_update_data)
        self.assertEqual(order_update.customerId, 1)
        self.assertEqual(order_update.status, 2)
        self.assertIsNone(order_update.createdAt)  # Vérifie que les champs non fournis sont None

    def test_order_product_update_valid(self):
        order_product_update_data = {
            "productId": 1,
            "quantity": 10
        }
        order_product_update = OrderProductUpdate(**order_product_update_data)
        self.assertEqual(order_product_update.productId, 1)
        self.assertEqual(order_product_update.quantity, 10)

    def test_customer_orders_response_valid(self):
        order_data = [
            {
                "id_order": 1,
                "createdAt": datetime.now(),
                "updated_at": datetime.now(),
                "status": 1
            }
        ]
        response_data = {
            "customer_id": 1,
            "orders": order_data
        }
        response = CustomerOrdersResponse(**response_data)
        self.assertEqual(response.customer_id, 1)
        self.assertEqual(len(response.orders), 1)
        self.assertEqual(response.orders[0].id_order, 1)

    def test_customer_orders_response_invalid(self):
        with self.assertRaises(ValidationError):
            CustomerOrdersResponse(customer_id="invalid", orders="not_a_list")

# Exécution des tests
if __name__ == '__main__':
    unittest.main()
