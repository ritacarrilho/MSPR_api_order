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

def copy_table(table_name):
    # Connexion aux bases de données
    source_connection = source_engine.connect()
    target_connection = target_engine.connect()

    try:
        # Charger uniquement la table spécifiée depuis la source
        print(f"Chargement de la table '{table_name}' depuis la base source...")
        source_metadata.reflect(bind=source_engine, only=[table_name])
        table = source_metadata.tables[table_name]

        # Vérifier l'existence de la table dans la base cible
        inspector = inspect(target_engine)
        target_tables = inspector.get_table_names()

        if table_name not in target_tables:
            print(f"Création de la table '{table_name}' dans la base cible...")
            table.create(bind=target_engine)

        # Copier les données de la table
        print(f"Copie des données de la table '{table_name}'...")
        rows = source_connection.execute(table.select()).fetchall()

        # Si des lignes existent, les afficher et tenter l'insertion
        if rows:
            print(f"Premières lignes extraites de {table_name} : {rows[:5]}")  # Afficher les 5 premières lignes pour débogage

            insert_rows = [dict(row) for row in rows]  # Conversion en dictionnaires

            with target_connection.begin() as transaction:  # Utilisation d'une transaction pour plus de sécurité
                target_table = Table(table_name, target_metadata, autoload_with=target_engine)
                insert_query = target_table.insert()
                target_connection.execute(insert_query, insert_rows)
        
        print(f"Copie de la table '{table_name}' terminée avec succès !")

    except SQLAlchemyError as e:
        print(f"SQLAlchemyError occurred while copying {table_name}: {e}")
    except Exception as e:
        print(f"Error occurred while copying {table_name}: {e}")
    finally:
        source_connection.close()
        target_connection.close()

def copy_tables():
    # Copier les tables 'order_products' et 'orders'
    copy_table('order_products')
    copy_table('orders')

if __name__ == "__main__":
    copy_tables()
