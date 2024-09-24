import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.controllers import (
    get_all_orders,
    get_order_by_id,
    create_order,
    update_order,
    delete_order,
    get_all_order_products,
    get_order_product_by_id,
    create_order_product,
    update_order_product,
    delete_order_product
)
from app.models import Order, OrderProduct
from app.schemas import OrderCreate, OrderUpdate, OrderProductCreate, OrderProductUpdate


class TestControllers(unittest.TestCase):

    def setUp(self):
        # Configuration de la base de données simulée
        self.db = MagicMock(Session)
        self.order_data = OrderCreate(customerId=1, createdAt="2023-09-01T12:00:00Z", status=0)
        self.order_product_data = OrderProductCreate(productId=1, quantity=2, id_order=1)

    def test_get_all_orders(self):
        self.db.query().all.return_value = [Order(id_order=1), Order(id_order=2)]
        orders = get_all_orders(self.db)
        self.assertEqual(len(orders), 2)

    def test_get_order_by_id_found(self):
        self.db.query().filter().first.return_value = Order(id_order=1)
        order = get_order_by_id(self.db, 1)
        self.assertEqual(order.id_order, 1)

    def test_get_order_by_id_not_found(self):
        self.db.query().filter().first.return_value = None
        with self.assertRaises(HTTPException) as context:
            get_order_by_id(self.db, 999)
        self.assertEqual(context.exception.status_code, 404)

    def test_create_order(self):
        self.db.add = MagicMock()
        self.db.commit = MagicMock()
        self.db.refresh = MagicMock()
        order = create_order(self.db, self.order_data)
        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()
        self.assertIsNotNone(order)

    def test_update_order_found(self):
        self.db.query().filter().first.return_value = Order(id_order=1, status=0)
        update_data = OrderUpdate(status=1)
        updated_order = update_order(self.db, 1, update_data)
        self.assertEqual(updated_order.status, 1)

    def test_update_order_not_found(self):
        self.db.query().filter().first.return_value = None
        update_data = OrderUpdate(status=1)
        with self.assertRaises(HTTPException) as context:
            update_order(self.db, 999, update_data)
        self.assertEqual(context.exception.status_code, 404)

    def test_delete_order_found(self):
        self.db.query().filter().first.return_value = Order(id_order=1)
        delete_order(self.db, 1)
        self.db.delete.assert_called_once()
        self.db.commit.assert_called_once()

    def test_delete_order_not_found(self):
        self.db.query().filter().first.return_value = None
        with self.assertRaises(HTTPException) as context:
            delete_order(self.db, 999)
        self.assertEqual(context.exception.status_code, 404)

    def test_get_all_order_products(self):
        self.db.query().all.return_value = [OrderProduct(id_order_products=1), OrderProduct(id_order_products=2)]
        products = get_all_order_products(self.db)
        self.assertEqual(len(products), 2)

    def test_get_order_product_by_id_found(self):
        self.db.query().filter().first.return_value = OrderProduct(id_order_products=1)
        product = get_order_product_by_id(self.db, 1)
        self.assertEqual(product.id_order_products, 1)

    def test_get_order_product_by_id_not_found(self):
        self.db.query().filter().first.return_value = None
        with self.assertRaises(HTTPException) as context:
            get_order_product_by_id(self.db, 999)
        self.assertEqual(context.exception.status_code, 404)

    def test_create_order_product(self):
        self.db.add = MagicMock()
        self.db.commit = MagicMock()
        self.db.refresh = MagicMock()
        order_product = create_order_product(self.db, self.order_product_data)
        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()
        self.assertIsNotNone(order_product)

    def test_update_order_product_found(self):
        self.db.query().filter().first.return_value = OrderProduct(id_order_products=1)
        update_data = OrderProductUpdate(quantity=3)
        updated_product = update_order_product(self.db, 1, update_data)
        self.assertEqual(updated_product.quantity, 3)

    def test_update_order_product_not_found(self):
        self.db.query().filter().first.return_value = None
        update_data = OrderProductUpdate(quantity=3)
        with self.assertRaises(HTTPException) as context:
            update_order_product(self.db, 999, update_data)
        self.assertEqual(context.exception.status_code, 404)

    def test_delete_order_product_found(self):
        self.db.query().filter().first.return_value = OrderProduct(id_order_products=1)
        delete_order_product(self.db, 1)
        self.db.delete.assert_called_once()
        self.db.commit.assert_called_once()

    def test_delete_order_product_not_found(self):
        self.db.query().filter().first.return_value = None
        with self.assertRaises(HTTPException) as context:
            delete_order_product(self.db, 999)
        self.assertEqual(context.exception.status_code, 404)


if __name__ == '__main__':
    unittest.main()
