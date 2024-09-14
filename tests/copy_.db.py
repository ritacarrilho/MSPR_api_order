import mysql.connector
from sqlalchemy import create_engine, MetaData, Table, inspect
from sqlalchemy.exc import SQLAlchemyError

# Configuration des connexions à la base de données
SOURCE_DB_URL = "mysql+mysqlconnector://root:@localhost:3306/order_db"
TARGET_DB_URL = "mysql+mysqlconnector://root:@localhost:3306/test_db"

source_engine = create_engine(SOURCE_DB_URL)
target_engine = create_engine(TARGET_DB_URL)

# Obtenir les métadonnées des bases de données
source_metadata = MetaData(bind=source_engine)
target_metadata = MetaData(bind=target_engine)

def copy_table_order_products():
    # Connexion aux bases de données
    source_connection = source_engine.connect()
    target_connection = target_engine.connect()

    try:
        # Charger uniquement la table 'order_products' depuis la source
        print("Chargement de la table 'order_products' depuis la base source...")
        source_metadata.reflect(bind=source_engine, only=['order_products'])
        order_products_table = source_metadata.tables['order_products']

        # Vérifier l'existence de la table dans la base cible
        inspector = inspect(target_engine)
        target_tables = inspector.get_table_names()

        if 'order_products' not in target_tables:
            print("Création de la table 'order_products' dans la base cible...")
            order_products_table.create(bind=target_engine)

        # Copier les données de la table 'order_products'
        print("Copie des données de la table 'order_products'...")
        rows = source_connection.execute(order_products_table.select()).fetchall()

        # Si des lignes existent, les afficher et tenter l'insertion
        if rows:
            print(f"Premières lignes extraites : {rows[:5]}")  # Afficher les 5 premières lignes pour débogage

            insert_rows = [dict(row) for row in rows]  # Conversion en dictionnaires

            with target_connection.begin() as transaction:  # Utilisation d'une transaction pour plus de sécurité
                target_table = Table('order_products', target_metadata, autoload_with=target_engine)
                insert_query = target_table.insert()
                target_connection.execute(insert_query, insert_rows)
        
        print("Copie de la table 'order_products' terminée avec succès !")

    except SQLAlchemyError as e:
        print(f"SQLAlchemyError occurred: {e}")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        source_connection.close()
        target_connection.close()

if __name__ == "__main__":
    copy_table_order_products()
