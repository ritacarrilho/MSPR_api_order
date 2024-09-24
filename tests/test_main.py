import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

class TestMain(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    @patch('app.controllers.get_all_orders')
    @patch('app.middleware.is_admin')
    def test_get_orders_success(self, mock_is_admin, mock_get_all_orders):
        mock_is_admin.return_value = None
        mock_get_all_orders.return_value = [{"id": 1, "customerId": 123, "status": "pending"}]

        response = self.client.get("/orders/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['id'], 1)

    @patch('app.controllers.get_all_orders')
    @patch('app.middleware.is_admin')
    def test_get_orders_no_orders(self, mock_is_admin, mock_get_all_orders):
        mock_is_admin.return_value = None
        mock_get_all_orders.return_value = []

        response = self.client.get("/orders/")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "No orders found"})

    @patch('app.controllers.get_order_by_id')
    @patch('app.middleware.is_customer_or_admin')
    def test_get_customer_orders_success(self, mock_is_customer_or_admin, mock_get_order_by_id):
        mock_get_order_by_id.return_value = {"id": 1, "customerId": 123, "status": "pending"}
        mock_is_customer_or_admin.return_value = None

        response = self.client.get("/orders/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], 1)

    @patch('app.controllers.get_order_by_id')
    def test_get_customer_orders_not_found(self, mock_get_order_by_id):
        mock_get_order_by_id.return_value = None

        response = self.client.get("/orders/999")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Order not found"})

    @patch('app.controllers.create_order')
    @patch('app.middleware.is_customer_or_admin')
    async def test_create_order_success(self, mock_is_customer_or_admin, mock_create_order):
        mock_create_order.return_value = {"id": 1, "customerId": 123, "status": "pending"}
        mock_is_customer_or_admin.return_value = None

        order_data = {"customerId": 123, "products": []}
        response = self.client.post("/orders/", json=order_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], 1)

    @patch('app.controllers.create_order')
    def test_create_order_error(self, mock_create_order):
        mock_create_order.side_effect = Exception("Error creating order")

        order_data = {"customerId": 123, "products": []}
        response = self.client.post("/orders/", json=order_data)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"detail": "An error occurred while creating the order"})


if __name__ == '__main__':
    unittest.main()
