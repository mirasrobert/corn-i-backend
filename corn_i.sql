/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

CREATE TABLE `soil_test` (
  `id` int NOT NULL AUTO_INCREMENT,
  `farm_site` varchar(200) NOT NULL,
  `client_name` varchar(200) NOT NULL,
  `lab_no` varchar(200) NOT NULL,
  `pH` float NOT NULL,
  `P` float NOT NULL,
  `K` float NOT NULL,
  `N` float NOT NULL,
  `MC` float NOT NULL,
  `date_reported` varchar(200) NOT NULL,
  `created_at` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(200) NOT NULL,
  `password` varchar(128) NOT NULL,
  `created_at` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `soil_test` (`id`, `farm_site`, `client_name`, `lab_no`, `pH`, `P`, `K`, `N`, `MC`, `date_reported`, `created_at`) VALUES
(6, 'Bukal Sur', 'Ishmael Vega', 'LAB-S0001', 4.05, 25, 17, 36, 7.05, '2023-04-19', '2023-04-20 06:29:39.399767');
INSERT INTO `soil_test` (`id`, `farm_site`, `client_name`, `lab_no`, `pH`, `P`, `K`, `N`, `MC`, `date_reported`, `created_at`) VALUES
(7, 'Malabanan Norte', 'Remedios Patrick', 'LAB-S0006', 4.08, 27, 18, 46, 8.05, '2023-04-17', '2023-04-20 08:22:38.616481');


INSERT INTO `user` (`id`, `email`, `password`, `created_at`) VALUES
(1, 'mrmirasrobert@gmail.com', '$2b$10$az63fHsR/g/2sWsE0HEeVuNgYBIqPDfmb9d9Wr/.E1OpfKCL7p7ZG', '2023-04-17 14:50:04.955414');
INSERT INTO `user` (`id`, `email`, `password`, `created_at`) VALUES
(2, 'mirasrobert@gmail.com', '$2b$10$/IA81eSN6xK3Uo1tdXNomuXvvuAKDfHz8BzomRrtM1X3fXKsp.XI.', '2023-04-18 09:05:28.056022');



/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;