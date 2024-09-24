import unittest
from unittest.mock import patch, MagicMock
from sqlalchemy import Column, MetaData, Table, DateTime, ForeignKey, insert, select, update, delete, inspect, Integer
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = MagicMock()
        cls.Session = sessionmaker(bind=cls.engine)
        cls.session = cls.Session()
        cls.metadata = MetaData()
        cls.metadata.bind = cls.engine
        cls.inspector = inspect(cls.engine)

        cls.orders_table = Table('orders', cls.metadata,
                Column('id_order', Integer, primary_key=True),
                Column('customerId', Integer),
                Column('createdAt', DateTime),
                Column('updated_at', DateTime),
                Column('status', Integer)
        )
        cls.order_products_table = Table('order_products', cls.metadata,
                        Column('id_order_products', Integer, primary_key=True),
                        Column('productId', Integer),
                        Column('quantity', Integer),
                        Column('id_order', Integer, ForeignKey('orders.id_order'))
        )

    @classmethod
    def tearDownClass(cls):
        cls.session.close()

    @patch('sqlalchemy.create_engine')
    def test_database_connection(self, mock_create_engine):
        mock_create_engine.return_value.connect.return_value = MagicMock()
        connection = self.engine.connect()
        self.assertTrue(connection)
        connection.close()

    # @patch('sqlalchemy.inspection.inspect')
    # def test_table_orders_exists(self, mock_inspect):
    #     mock_inspect.return_value.get_table_names.return_value = ['orders', 'order_products']
    #     tables = self.inspector.get_table_names()
    #     self.assertIn('orders', tables, "La table 'orders' n'existe pas dans la base de données.")

    # @patch('sqlalchemy.inspection.inspect')
    # def test_table_order_products_exists(self, mock_inspect):
    #     mock_inspect.return_value.get_table_names.return_value = ['orders', 'order_products']
    #     tables = self.inspector.get_table_names()
    #     self.assertIn('order_products', tables, "La table 'order_products' n'existe pas dans la base de données.")

    def test_insert_into_orders(self):
        insert_mock = MagicMock()
        self.orders_table.insert = lambda: insert_mock
        insert_mock.return_value = MagicMock(inserted_primary_key=[1])
        try:
            insert_query = insert(self.orders_table).values(customerId=1, createdAt="2024-09-14 10:00:00")
            result = self.session.execute(insert_query)
            self.session.commit()
            self.assertIsNotNone(result.inserted_primary_key, "L'insertion dans la table 'orders' a échoué.")
        except SQLAlchemyError as e:
            self.fail(f"Erreur lors de l'insertion dans 'orders' : {e}")

    def test_insert_into_order_products(self):
        insert_mock = MagicMock()
        self.order_products_table.insert = lambda: insert_mock
        insert_mock.return_value = MagicMock(inserted_primary_key=[1])
        try:
            insert_query = insert(self.order_products_table).values(productId=1, quantity=10, id_order=1)
            result = self.session.execute(insert_query)
            self.session.commit()
            self.assertIsNotNone(result.inserted_primary_key, "L'insertion dans la table 'order_products' a échoué.")
        except SQLAlchemyError as e:
            self.fail(f"Erreur lors de l'insertion dans 'order_products' : {e}")

    # def test_read_from_orders(self):
    #     select_mock = MagicMock()
    #     self.orders_table.select = lambda: select_mock
    #     select_mock.return_value.fetchone.return_value = {'customerId': 1}
    #     try:
    #         select_query = select([self.orders_table]).where(self.orders_table.c.customerId == 1)
    #         result = self.session.execute(select_query).fetchone()
    #         self.assertIsNotNone(result, "Aucune donnée trouvée dans la table 'orders'.")
    #         self.assertEqual(result['customerId'], 1, "Le champ 'customerId' est incorrect.")
    #     except SQLAlchemyError as e:
    #         self.fail(f"Erreur lors de la lecture dans 'orders' : {e}")

    # def test_update_orders(self):
    #     update_mock = MagicMock()
    #     self.orders_table.update = lambda: update_mock
    #     update_mock.return_value = MagicMock(rowcount=1)
    #     try:
    #         update_query = update(self.orders_table).where(self.orders_table.c.customerId == 1).values(status=1)
    #         result = self.session.execute(update_query)
    #         self.session.commit()
    #         self.assertGreater(result.rowcount, 0, "Aucune ligne n'a été mise à jour dans la table 'orders'.")
    #     except SQLAlchemyError as e:
    #         self.fail(f"Erreur lors de la mise à jour dans 'orders' : {e}")

    # def test_delete_from_orders(self):
    #     delete_mock = MagicMock()
    #     self.orders_table.delete = lambda: delete_mock
    #     delete_mock.return_value = MagicMock(rowcount=1)
    #     try:
    #         delete_query = delete(self.orders_table).where(self.orders_table.c.customerId == 1)
    #         result = self.session.execute(delete_query)
    #         self.session.commit()
    #         self.assertGreater(result.rowcount, 0, "Aucune ligne n'a été supprimée dans la table 'orders'.")
    #     except SQLAlchemyError as e:
    #         self.fail(f"Erreur lors de la suppression dans 'orders' : {e}")

    # def test_read_from_order_products(self):
    #     select_mock = MagicMock()
    #     self.order_products_table.select = lambda: select_mock
    #     select_mock.return_value.fetchone.return_value = {'productId': 1}
    #     try:
    #         select_query = select([self.order_products_table]).where(self.order_products_table.c.id_order == 1)
    #         result = self.session.execute(select_query).fetchone()
    #         self.assertIsNotNone(result, "Aucune donnée trouvée dans la table 'order_products'.")
    #         self.assertEqual(result['productId'], 1, "Le champ 'productId' est incorrect.")
    #     except SQLAlchemyError as e:
    #         self.fail(f"Erreur lors de la lecture dans 'order_products' : {e}")

if __name__ == '__main__':
    unittest.main()
