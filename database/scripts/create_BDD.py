import mysql.connector
from mysql.connector import errorcode
import json
import os

# Informations de connexion MySQL
config = {
    'user': 'root',      
    'password': '',      
    'host': 'localhost', 
}

# Nom de la base de données
db_name = 'order_db'

# Chemin du fichier JSON
json_file_path = os.path.join('..', 'data', 'data.json')

# Connexion à MySQL
try:
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    # Suppression de la base de données si elle existe déjà
    try:
        cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
        print(f"La base de données '{db_name}' a été supprimée.")
    except mysql.connector.Error as err:
        print(f"Erreur lors de la suppression de la base de données : {err}")

    # Création de la base de données
    try:
        cursor.execute(f"CREATE DATABASE {db_name} DEFAULT CHARACTER SET 'utf8'")
        print(f"La base de données '{db_name}' a été créée avec succès.")
    except mysql.connector.Error as err:
        print(f"Erreur lors de la création de la base de données : {err}")
        if err.errno == errorcode.ER_DB_CREATE_EXISTS:
            print(f"La base de données '{db_name}' existe déjà.")
        else:
            print(err)

    # Sélectionner la base de données
    cursor.execute(f"USE {db_name}")

    # Définir les requêtes de création des tables
    create_tables_queries = {
        'Orders': """
            CREATE TABLE orders (
                id_order INT,
                customerId INT NOT NULL,
                createdAt DATETIME NOT NULL,
                PRIMARY KEY (id_order)
            )
        """,
        'Order_Products': """
            CREATE TABLE order_products (
                id_order_products INT AUTO_INCREMENT,
                productId INT NOT NULL,
                quantity INT NOT NULL,
                id_order INT NOT NULL,
                PRIMARY KEY (id_order_products),
                FOREIGN KEY (id_order) REFERENCES orders(id_order)
            )
        """
    }

    # Création des tables
    for table_name, create_query in create_tables_queries.items():
        try:
            cursor.execute(create_query)
            print(f"Table '{table_name}' créée avec succès.")
        except mysql.connector.Error as err:
            print(f"Erreur lors de la création de la table {table_name} : {err}")

    # Lecture des données du fichier JSON
    try:
        with open(json_file_path, 'r') as f:
            data = json.load(f)

        # Insertion des données dans la table Orders et Order_Products
        for order in data:
            # Insertion des ordres dans la table Orders
            insert_order = """
                INSERT INTO orders (id_order, customerId, createdAt)
                VALUES (%s, %s, %s)
            """
            cursor.execute(insert_order, (
                order['id'],
                order['customerId'],
                order['createdAt']
            ))

            # Insertion des produits associés à chaque ordre dans la table Order_Products
            for product in order['products']:
                insert_order_product = """
                    INSERT INTO order_products (productId, quantity, id_order)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(insert_order_product, (
                    product['id'],  # id du produit
                    product['stock'],  # prb quantité compter nombre de fois le produit sinon on à pas l'info haha FUCK !
                    order['id']  
                ))

        # Valider les changements
        cnx.commit()
        print("Données insérées avec succès.")

    except FileNotFoundError:
        print(f"Le fichier {json_file_path} n'existe pas.")
    except json.JSONDecodeError as e:
        print(f"Erreur de décodage JSON : {e}")
    except mysql.connector.Error as err:
        print(f"Erreur lors de l'insertion des données : {err}")

    # Fermer la connexion
    cursor.close()
    cnx.close()

except mysql.connector.Error as err:
    print(f"Erreur de connexion à MySQL : {err}")