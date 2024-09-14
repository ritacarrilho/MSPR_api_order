import unittest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app
from datetime import datetime, timezone

# Configuration de la base de données de test MySQL
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:@localhost:3306/test_db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dépendance pour la base de données dans les tests
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def get_current_time():
    return datetime.now(timezone.utc).isoformat()

class TestAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Créer toutes les tables dans la base de données avant les tests
        Base.metadata.create_all(bind=engine)

    @classmethod
    def tearDownClass(cls):
        # Supprimer toutes les tables après les tests
        Base.metadata.drop_all(bind=engine)

    def test_create_order(self):
        order_data = {
            "customerId": 1,  # Mise à jour du nom du champ
            "createdAt": get_current_time(),
            "updated_at": get_current_time(),
            "status": "0"  # Mise à jour du type de champ
        }
        response = client.post("/orders/", json=order_data)
        print("Create Order Response:", response.json())  # Debug
        self.assertEqual(response.status_code, 200)
        self.assertIn("id_order", response.json())  # Vérifie que l'ID est présent
        self.assertEqual(response.json()["status"], "0")

    def test_get_orders(self):
        response = client.get("/orders/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_update_order(self):
        # Crée une commande pour tester la mise à jour
        order_data = {
            "customerId": 1,  # Mise à jour du nom du champ
            "createdAt": get_current_time(),
            "updated_at": get_current_time(),
            "status": "0"  # Mise à jour du type de champ
        }
        create_response = client.post("/orders/", json=order_data)
        created_order = create_response.json()
        print("Create Order Response for Update:", created_order)  # Debug
        order_id = created_order.get("id_order")

        # Met à jour la commande
        update_data = {
            "status": "1"  # Mise à jour du type de champ
        }
        response = client.patch(f"/orders/{order_id}", json=update_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "1")

    def test_delete_order(self):
        # Crée une commande pour tester la suppression
        order_data = {
            "customerId": 1,  # Mise à jour du nom du champ
            "createdAt": get_current_time(),
            "updated_at": get_current_time(),
            "status": "0"  # Mise à jour du type de champ
        }
        create_response = client.post("/orders/", json=order_data)
        created_order = create_response.json()
        print("Create Order Response for Delete:", created_order)  # Debug
        order_id = created_order.get("id_order")

        # Supprime la commande
        response = client.delete(f"/orders/{order_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["detail"], "Order deleted")

        # Vérifie que la commande a été supprimée
        get_response = client.get(f"/orders/{order_id}")
        self.assertEqual(get_response.status_code, 404)

if __name__ == "__main__":
    unittest.main()
