import unittest
from sqlalchemy import create_engine, MetaData, Table, insert, select, update, delete, inspect
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine('mysql+mysqlconnector://orders:kawaorders@kawa-orders-db:3306/order_db')
        # cls.engine = create_engine("mysql+mysqlconnector://root:@localhost:3306/test_db")
        cls.Session = sessionmaker(bind=cls.engine)
        cls.session = cls.Session()
        cls.metadata = MetaData(bind=cls.engine)
        cls.inspector = inspect(cls.engine)
        
        # Charger les tables nécessaires
        cls.orders_table = Table('orders', cls.metadata, autoload_with=cls.engine)
        cls.order_products_table = Table('order_products', cls.metadata, autoload_with=cls.engine)

    @classmethod
    def tearDownClass(cls):
        cls.session.close()

    # Test de connexion à la base de données
    def test_database_connection(self):
        """Teste la connexion à la base de données."""
        try:
            connection = self.engine.connect()
            self.assertTrue(connection)
        except SQLAlchemyError as e:
            self.fail(f"Erreur de connexion à la base de données : {e}")
        finally:
            connection.close()

    # Test pour vérifier l'existence de la table 'orders'
    def test_table_orders_exists(self):
        """Vérifie que la table 'orders' existe dans test_db."""
        try:
            tables = self.inspector.get_table_names()
            self.assertIn('orders', tables, "La table 'orders' n'existe pas dans la base de données.")
        except SQLAlchemyError as e:
            self.fail(f"Erreur SQLAlchemy lors de la vérification de l'existence de la table 'orders' : {e}")

    # Test pour vérifier l'existence de la table 'order_products'
    def test_table_order_products_exists(self):
        """Vérifie que la table 'order_products' existe dans test_db."""
        try:
            tables = self.inspector.get_table_names()
            self.assertIn('order_products', tables, "La table 'order_products' n'existe pas dans la base de données.")
        except SQLAlchemyError as e:
            self.fail(f"Erreur SQLAlchemy lors de la vérification de l'existence de la table 'order_products' : {e}")

    # Test pour insérer des données dans la table 'orders'
    def test_insert_into_orders(self):
        """Teste l'insertion d'une commande dans la table 'orders'."""
        try:
            insert_query = insert(self.orders_table).values(customerId=1, createdAt="2024-09-14 10:00:00")
            result = self.session.execute(insert_query)
            self.session.commit()
            
            # Vérifier que l'insertion a réussi
            self.assertIsNotNone(result.inserted_primary_key, "L'insertion dans la table 'orders' a échoué.")
        except SQLAlchemyError as e:
            self.fail(f"Erreur lors de l'insertion dans 'orders' : {e}")

    # Test pour insérer des données dans la table 'order_products'
    def test_insert_into_order_products(self):
        """Teste l'insertion d'un produit dans la table 'order_products'."""
        try:
            insert_query = insert(self.order_products_table).values(productId=1, quantity=10, id_order=1)
            result = self.session.execute(insert_query)
            self.session.commit()
            
            # Vérifier que l'insertion a réussi
            self.assertIsNotNone(result.inserted_primary_key, "L'insertion dans la table 'order_products' a échoué.")
        except SQLAlchemyError as e:
            self.fail(f"Erreur lors de l'insertion dans 'order_products' : {e}")

    # Test pour lire des données dans la table 'orders'
    def test_read_from_orders(self):
        """Teste la lecture des données insérées dans la table 'orders'."""
        try:
            select_query = select([self.orders_table]).where(self.orders_table.c.customerId == 1)
            result = self.session.execute(select_query).fetchone()
            
            # Vérifier que les données sont bien récupérées
            self.assertIsNotNone(result, "Aucune donnée trouvée dans la table 'orders'.")
            self.assertEqual(result['customerId'], 1, "Le champ 'customerId' est incorrect.")
        except SQLAlchemyError as e:
            self.fail(f"Erreur lors de la lecture dans 'orders' : {e}")

    # Test pour mettre à jour des données dans la table 'orders'
    def test_update_orders(self):
        """Teste la mise à jour d'une commande dans la table 'orders'."""
        try:
            update_query = update(self.orders_table).where(self.orders_table.c.customerId == 1).values(status=1)
            result = self.session.execute(update_query)
            self.session.commit()

            # Vérifier que la mise à jour a réussi
            self.assertGreater(result.rowcount, 0, "Aucune ligne n'a été mise à jour dans la table 'orders'.")
        except SQLAlchemyError as e:
            self.fail(f"Erreur lors de la mise à jour dans 'orders' : {e}")

    # Test pour supprimer des données dans la table 'orders'
    def test_delete_from_orders(self):
        """Teste la suppression d'une commande dans la table 'orders'."""
        try:
            delete_query = delete(self.orders_table).where(self.orders_table.c.customerId == 1)
            result = self.session.execute(delete_query)
            self.session.commit()

            # Vérifier que la suppression a réussi
            self.assertGreater(result.rowcount, 0, "Aucune ligne n'a été supprimée dans la table 'orders'.")
        except SQLAlchemyError as e:
            self.fail(f"Erreur lors de la suppression dans 'orders' : {e}")

    # Test pour lire des données dans la table 'order_products'
    def test_read_from_order_products(self):
        """Teste la lecture des données insérées dans la table 'order_products'."""
        try:
            select_query = select([self.order_products_table]).where(self.order_products_table.c.id_order == 1)
            result = self.session.execute(select_query).fetchone()
            
            # Vérifier que les données sont bien récupérées
            self.assertIsNotNone(result, "Aucune donnée trouvée dans la table 'order_products'.")
            self.assertEqual(result['productId'], 1, "Le champ 'productId' est incorrect.")
        except SQLAlchemyError as e:
            self.fail(f"Erreur lors de la lecture dans 'order_products' : {e}")

if __name__ == '__main__':
    unittest.main()
