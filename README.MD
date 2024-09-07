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
### Détails tables



## Endpoints de l'API



## Docker

1) Build container : ```docker-compose build```

2) Test avec coverage : ```docker-compose up```


## Commandes utiles
### Effacer fichiers DS_Store
```java
find . -name .DS_Store -print0 | xargs -0 git rm -f --ignore-unmatch
```
