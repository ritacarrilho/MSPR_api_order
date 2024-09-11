<<<<<<< HEAD
-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : mer. 11 sep. 2024 à 22:33
-- Version du serveur : 8.0.31
-- Version de PHP : 8.1.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `order_db`
--

-- --------------------------------------------------------

--
-- Structure de la table `orders`
--

DROP TABLE IF EXISTS `orders`;
CREATE TABLE IF NOT EXISTS `orders` (
  `id_order` int NOT NULL AUTO_INCREMENT,
  `customerId` int NOT NULL,
  `createdAt` datetime NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  `status` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_order`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `orders`
--

INSERT INTO `orders` (`id_order`, `customerId`, `createdAt`, `updated_at`, `status`) VALUES
(1, 1, '2023-09-01 10:00:00', '2023-09-01 10:00:00', 1),
(2, 2, '2023-09-02 11:30:00', '2023-09-02 11:30:00', 0),
(3, 1, '2023-09-03 14:15:00', '2023-09-03 14:15:00', 1);

-- --------------------------------------------------------

--
-- Structure de la table `order_products`
--

DROP TABLE IF EXISTS `order_products`;
CREATE TABLE IF NOT EXISTS `order_products` (
  `id_order_products` int NOT NULL AUTO_INCREMENT,
  `productId` int NOT NULL,
  `quantity` int NOT NULL,
  `id_order` int NOT NULL,
  PRIMARY KEY (`id_order_products`),
  KEY `id_order` (`id_order`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `order_products`
--

INSERT INTO `order_products` (`id_order_products`, `productId`, `quantity`, `id_order`) VALUES
(1, 1, 2, 1),
(2, 2, 1, 1),
(3, 3, 3, 2),
(4, 2, 1, 3),
(5, 1, 5, 3);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
=======
CREATE TABLE orders(
   id_order INT AUTO_INCREMENT,
   customerId INT NOT NULL,
   createdAt DATETIME NOT NULL,
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

INSERT INTO orders (id_order, customerId, createdAt) VALUES
(1, 7, '2023-08-30 10:54:50'),
(2, 10, '2023-08-30 13:29:29'),
(3, 11, '2023-08-30 08:35:27'),
(4, 12, '2023-08-29 19:21:39'),
(5, 13, '2023-08-29 21:22:06'),
(6, 14, '2023-08-30 13:52:46'),
(7, 15, '2023-08-29 16:24:29'),
(8, 16, '2023-08-30 03:56:35'),
(9, 17, '2023-08-29 21:41:14'),
(10, 18, '2023-08-29 19:58:55'),
(11, 19, '2023-08-30 04:18:18'),
(12, 20, '2023-08-29 23:00:30'),
(13, 21, '2023-08-30 03:11:48'),
(14, 22, '2023-08-30 08:53:35'),
(15, 23, '2023-08-29 18:36:04'),
(16, 24, '2023-08-30 04:16:00'),
(17, 26, '2023-08-30 08:29:14'),
(18, 27, '2023-08-29 23:45:25'),
(19, 28, '2023-08-30 13:00:17'),
(20, 29, '2023-08-29 17:26:18'),
(21, 30, '2023-08-30 02:49:37'),
(22, 31, '2023-08-30 09:58:24'),
(23, 32, '2023-08-29 20:37:10'),
(24, 33, '2023-08-30 02:36:03'),
(25, 34, '2023-08-30 04:09:31'),
(26, 35, '2023-08-30 03:26:12'),
(27, 36, '2023-08-30 03:26:12'),
(28, 37, '2023-08-29 15:50:11'),
(29, 38, '2023-08-29 21:41:14'),
(30, 39, '2023-08-29 21:51:40');

INSERT INTO order_products (productId, quantity, id_order) VALUES
(1, 16996, 1),
(51, 46781, 1),
(2, 29484, 2),
(52, 69371, 2),
(3, 73253, 3),
(53, 1609, 3),
(4, 6547, 4),
(54, 45915, 4),
(5, 94846, 5),
(55, 91337, 5),
(6, 12617, 6),
(56, 4268, 6),
(7, 8057, 7),
(57, 97744, 7),
(8, 79359, 8),
(58, 30266, 8),
(9, 33989, 9),
(59, 88417, 9),
(10, 42497, 10),
(60, 91778, 10),
(11, 33257, 11),
(61, 8377, 11),
(12, 56401, 12),
(62, 85808, 12),
(13, 84061, 13),
(63, 53921, 13),
(14, 85648, 14),
(64, 46969, 14),
(15, 53324, 15),
(65, 2566, 15),
(16, 86472, 16),
(66, 40406, 16),
(17, 59785, 17),
(67, 40750, 17),
(18, 53995, 18),
(68, 42387, 18),
(19, 18076, 19),
(69, 10534, 19),
(20, 59882, 20),
(70, 22415, 20),
(21, 69357, 21),
(71, 49232, 21),
(22, 68826, 22),
(72, 33102, 22),
(23, 34570, 23),
(73, 4488, 23),
(24, 73622, 24),
(74, 49933, 24),
(25, 39977, 25),
(75, 41487, 25),
(26, 63253, 26),
(76, 3549, 26);
>>>>>>> f646b989f765bebbe137ff096ccc3ca701f16cc5
