## Kawa Orders API 
![](/assets/payetonkawaBanner.png)

## Participants 👥
- BILLARD Mélissa
- BRACCIALES-COMBAS Lola
- CARRILHO LAMEIRA Rita
- DIAGNE Sokhna

## Technologie 
- Api en [FastApi](https://fastapi.tiangolo.com/)

## Base de données
[MySQL](https://www.mysql.com/fr/)

**Nom BDD** : ``order_db``

### Création de la base de donnée
```python
## De la racine 
py database/scripts/create_BDD.py
```
![](/assets/create_bdd-2.png)

### Mock initial
```
https://615f5fb4f7254d0017068109.mockapi.io/api/v1/orders
```
*Liste de données de toutes les commandes*

![](/assets/mock.png)

### Modèle Conceptuel de Données (MCD)
![](/assets/mcd-2.png)

#### Modèle Logique de Données (MLD)
![](/assets/mld-2.png)

### Détails tables

#### Table ``orders``

id_order (INT, clé primaire) : Identifiant unique pour chaque commande. 

customerId (INT) : Identifiant du client qui a passé la commande. 

*Ce champ fait référence à l'ID du client dans le microservice de gestion des clients. Il permet d'associer chaque commande à un client spécifique.*

createdAt (TIMESTAMP) : Date et heure de création de la commande. 

#### Table ``order_products``

id_order_products (INT, clé primaire) : Identifiant unique de l'entrée de produit dans la commande.

orderId (INT) : Identifiant de la commande à laquelle ce produit est associé. 

*Ce champ fait référence à l'ID de la commande dans la table orders, permettant de lier chaque produit à sa commande correspondante.*

productId (INT) : Identifiant du produit commandé. 

*Ce champ fait référence à l'ID du produit dans le microservice de gestion des produits. Il permet d'associer chaque produit à sa description et ses détails dans le microservice approprié.*

quantity (INT) : Quantité de ce produit dans la commande. 

*Ce champ indique combien d'unités du produit ont été commandées, essentiel pour la gestion des stocks et le traitement des commandes.*

## Endpoints de l'API
![](/assets/api-endpoint.png)


## Docker

1) Build container : ```docker-compose build```

2) Test avec coverage : ```docker-compose up```


## Commandes utiles

### Lancer l'api en local
```python
# Dans le fichier app
fastapi dev main.py
# ou
# À la racine
 uvicorn app.main:app --reload
```

### Effacer fichiers DS_Store
```java
find . -name .DS_Store -print0 | xargs -0 git rm -f --ignore-unmatch
```

## Tests
Librairie utilisé : [unittest](https://docs.python.org/3/library/unittest.html)
```python
pip install fastapi requests sqlalchemy
```

Exécuter les tests : 
```python
python -m unittest tests/test_api.py
```
### Tests unitaires et d'intégration

![](/assets/test-ok.png)

| Test | Description | Type de Test |
|------|-------------|--------------|
| `test_database_connection` | Teste la connexion à la base de données. | Unitaire |
| `test_table_orders_exists` | Vérifie que la table 'orders' existe dans `test_db`. | Unitaire |
| `test_table_order_products_exists` | Vérifie que la table 'order_products' existe dans `test_db`. | Unitaire |
| `test_insert_into_orders` | Teste l'insertion d'une commande dans la table 'orders'. | Intégration |
| `test_insert_into_order_products` | Teste l'insertion d'un produit dans la table 'order_products'. | Intégration |
| `test_read_from_orders` | Teste la lecture des données insérées dans la table 'orders'. | Intégration |
| `test_update_orders` | Teste la mise à jour d'une commande dans la table 'orders'. | Intégration |
| `test_delete_from_orders` | Teste la suppression d'une commande dans la table 'orders'. | Intégration |
| `test_read_from_order_products` | Teste la lecture des données insérées dans la table 'order_products'. | Intégration |

#### Rapport de test en format XML
```python
pytest --junitxml=report.xml
```
#### Rapport de test en format HTML
```python
coverage run -m unittest discover
coverage report
coverage html
```
![](/assets/coverage.png)
