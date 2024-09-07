## Kawa Orders API 

## Participants 👥
- BILLARD Mélissa
- BRACCIALES-COMBAS Lola
- CARRILHO LAMEIRA Rita

## Technologie 
- Api en [FastApi](https://fastapi.tiangolo.com/)

## Base de données
(MySQL)[https://www.mysql.com/fr/]

**Nom BDD** : ``order_db``

### Création de la base de donnée
```python
py .\create_BDD.py
```
![](/assets/create_bdd.png)

### Mock initial
```
https://615f5fb4f7254d0017068109.mockapi.io/api/v1/orders
```
*Liste de données de toutes les commandes*

![](/assets/mock.png)

### Modèle conceptuel de données (MCD)
![](/assets/mcd.png)

### Détails tables

#### Table ``orders``

id_order (INT, clé primaire) : Identifiant unique pour chaque commande. 

customerId (INT) : Identifiant du client qui a passé la commande. 

*Ce champ fait référence à l'ID du client dans le microservice de gestion des clients. Il permet d'associer chaque commande à un client spécifique.*

createdAt (TIMESTAMP) : Date et heure de création de la commande. 

*Ce champ enregistre le moment où la commande a été passée, ce qui est utile pour le suivi et l'historique des commandes.*





## Endpoints de l'API


## Docker

1) Build container : ```docker-compose build```

2) Test avec coverage : ```docker-compose up```


## Commandes utiles
### Effacer fichiers DS_Store
```java
find . -name .DS_Store -print0 | xargs -0 git rm -f --ignore-unmatch
```
