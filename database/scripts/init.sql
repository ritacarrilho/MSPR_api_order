  CREATE TABLE orders(
   id_order INT AUTO_INCREMENT,
   customerId INT NOT NULL,
   createdAt DATETIME NOT NULL,
   updated_at DATETIME,
   status INT NOT NULL DEFAULT 0,
   PRIMARY KEY(id_order)
);

CREATE TABLE order_products(
   id_order_products INT AUTO_INCREMENT,
   productId INT NOT NULL,
   quantity INT NOT NULL,
   id_order INT NOT NULL,
   PRIMARY KEY(id_order_products),
   FOREIGN KEY(id_order) REFERENCES orders(id_order)
);

-- Insertion de données dans la table des commandes
INSERT INTO orders (customerId, createdAt, updated_at, status) VALUES
(1, '2023-09-01 10:00:00', '2023-09-01 10:00:00', 1),  
(2, '2023-09-02 11:30:00', '2023-09-02 11:30:00', 0),  
(1, '2023-09-03 14:15:00', '2023-09-03 14:15:00', 1);  

-- Insertion de données dans la table des produits de commande
INSERT INTO order_products (productId, quantity, id_order) VALUES
(1, 2, 1),  
(2, 1, 1),  
(3, 3, 2),  
(2, 1, 3),  
(1, 5, 3);  