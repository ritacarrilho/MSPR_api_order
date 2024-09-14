import unittest
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker

# Configuration de la base de données de test
TEST_DB_URL = "mysql+mysqlconnector://root:@localhost:3306/test_db"
engine = create_engine(TEST_DB_URL)
metadata = MetaData(bind=engine)

# Création d'une session
Session = sessionmaker(bind=engine)
session = Session()

class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Cette méthode est exécutée une seule fois avant tous les tests."""
        # Chargement des métadonnées
        cls.connection = engine.connect()
        cls.metadata = MetaData(bind=engine)
        cls.metadata.reflect(bind=engine)
        cls.session = session

    @classmethod
    def tearDownClass(cls):
        """Cette méthode est exécutée une seule fois après tous les tests."""
        cls.session.close()
        cls.connection.close()

    def test_table_orders_exists(self):
        """Vérifie que la table 'orders' existe dans test_db."""
        inspector = engine.dialect.get_inspector(engine)
        tables = inspector.get_table_names()
        self.assertIn('orders', tables, "La table 'orders' devrait exister dans la base de données.")

    def test_table_order_products_exists(self):
        """Vérifie que la table 'order_products' existe dans test_db."""
        inspector = engine.dialect.get_inspector(engine)
        tables = inspector.get_table_names()
        self.assertIn('order_products', tables, "La table 'order_products' devrait exister dans la base de données.")

    def test_insert_data_into_orders(self):
        """Test l'insertion de données dans la table 'orders'."""
        # Sélection de la table
        orders = Table('orders', self.metadata, autoload_with=engine)

        # Insertion de données exemple
        ins = orders.insert().values(customerId=1, createdAt='2023-09-14 10:00:00', status=1)
        result = self.connection.execute(ins)
        self.assertTrue(result.rowcount > 0, "L'insertion dans 'orders' a échoué.")

    def test_insert_data_into_order_products(self):
        """Test l'insertion de données dans la table 'order_products'."""
        # Assurez-vous qu'une commande existe dans la table 'orders' pour la clé étrangère
        orders = Table('orders', self.metadata, autoload_with=engine)
        order_ins = orders.insert().values(customerId=1, createdAt='2023-09-14 10:00:00', status=1)
        result = self.connection.execute(order_ins)
        id_order = result.inserted_primary_key[0]

        # Sélection de la table 'order_products'
        order_products = Table('order_products', self.metadata, autoload_with=engine)

        # Insertion de données dans 'order_products'
        ins = order_products.insert().values(productId=1, quantity=10, id_order=id_order)
        result = self.connection.execute(ins)
        self.assertTrue(result.rowcount > 0, "L'insertion dans 'order_products' a échoué.")

    def test_query_order_products(self):
        """Test une requête sur la table 'order_products'."""
        order_products = Table('order_products', self.metadata, autoload_with=engine)
        query = order_products.select()
        result = self.connection.execute(query).fetchall()

        # Vérifier que le résultat contient des données
        self.assertTrue(len(result) > 0, "Aucune donnée trouvée dans 'order_products'.")

if __name__ == "__main__":
    unittest.main()
