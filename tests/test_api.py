import unittest
from sqlalchemy import create_engine, MetaData, inspect
from sqlalchemy.exc import SQLAlchemyError

class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine("mysql+mysqlconnector://root:@localhost:3306/test_db")
        cls.connection = cls.engine.connect()
        cls.metadata = MetaData(bind=cls.engine)
        cls.inspector = inspect(cls.engine)

    @classmethod
    def tearDownClass(cls):
        cls.connection.close()

    def test_table_orders_exists(self):
        """Vérifie que la table 'orders' existe dans test_db."""
        try:
            tables = self.inspector.get_table_names()
            self.assertIn('orders', tables, "La table 'orders' n'existe pas dans la base de données.")
        except SQLAlchemyError as e:
            self.fail(f"Erreur SQLAlchemy lors de la vérification de l'existence de la table 'orders' : {e}")
        except Exception as e:
            self.fail(f"Erreur lors de la vérification de la table 'orders' : {e}")

    def test_table_order_products_exists(self):
        """Vérifie que la table 'order_products' existe dans test_db."""
        try:
            tables = self.inspector.get_table_names()
            self.assertIn('order_products', tables, "La table 'order_products' n'existe pas dans la base de données.")
        except SQLAlchemyError as e:
            self.fail(f"Erreur SQLAlchemy lors de la vérification de l'existence de la table 'order_products' : {e}")
        except Exception as e:
            self.fail(f"Erreur lors de la vérification de la table 'order_products' : {e}")

    # Vous pouvez ajouter plus de tests pour l'insertion, la mise à jour ou la suppression de données ici.

if __name__ == '__main__':
    unittest.main()
