-- MariaDB dump 10.19  Distrib 10.5.18-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: ai_fish
-- ------------------------------------------------------
-- Server version	10.5.18-MariaDB-0+deb11u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `dispenser`
--

DROP TABLE IF EXISTS `dispenser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dispenser` (
  `dispenser_ID` int(11) NOT NULL AUTO_INCREMENT,
  `field_ID` int(11) DEFAULT NULL,
  PRIMARY KEY (`dispenser_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dispenser`
--

LOCK TABLES `dispenser` WRITE;
/*!40000 ALTER TABLE `dispenser` DISABLE KEYS */;
INSERT INTO `dispenser` VALUES (1,1),(2,1);
/*!40000 ALTER TABLE `dispenser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fcr`
-- `fcr`: 換肉率
--

DROP TABLE IF EXISTS `fcr`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fcr` (
  `field_ID` int(11) DEFAULT NULL,
  `fcr` float DEFAULT NULL,
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fcr`
--

LOCK TABLES `fcr` WRITE;
/*!40000 ALTER TABLE `fcr` DISABLE KEYS */;
INSERT INTO `fcr` VALUES (1,2,'2023-03-12 11:13:42','2023-03-12 11:15:48');
/*!40000 ALTER TABLE `fcr` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `field_logs`
--

DROP TABLE IF EXISTS `field_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `field_logs` (
  `pool_ID` int(11) NOT NULL,
  `spec` float DEFAULT NULL,
  `record_weights` float DEFAULT NULL,
  `estimated_weights` float DEFAULT NULL,
  `fcr` float DEFAULT NULL,
  `dead_counts` int(11) DEFAULT NULL,
  `update_time` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/* `spec`: 尾/公斤 */
--
-- Dumping data for table `field_logs`
--

LOCK TABLES `field_logs` WRITE;
/*!40000 ALTER TABLE `field_logs` DISABLE KEYS */;
INSERT INTO `field_logs` VALUES (1,100.0,300.0,300.0,0.0,0,'2023-03-01 12:30:00'),(1,50.0,600.0,600.0,1.5,100,'2023-04-01 12:30:00');
INSERT INTO `field_logs` VALUES (2,120.0,300.0,300.0,0.0,0,'2023-03-02 12:00:00'),(2,90.0,400.0,400.0,2.0,100,'2023-03-10 12:20:00'),(2,60.0,600.0,600.0,2.0,100,'2023-04-01 12:40:00');
INSERT INTO `field_logs` VALUES (3,145.0,500.0,500.0,0.0,0,'2023-03-03 12:45:00'),(3,98.0,850.0,900.0,1.2,100,'2023-04-04 12:00:00');
/*!40000 ALTER TABLE `field_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ESP32`
--
DROP TABLE IF EXISTS `ESP32`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ESP32` (
  `dispenser_ID` int(11) NOT NULL default '1',
  `weight` float(10,2) DEFAULT NULL,
  `laser` float(10,2) DEFAULT NULL,
  `blower_state` varchar(255) DEFAULT NULL,
  `angle_state` varchar(255) DEFAULT NULL,
  `speed_level` varchar(255) DEFAULT NULL,
  `system_mode` varchar(255) DEFAULT NULL,
  `time` time DEFAULT NULL,
  `date` date DEFAULT NULL
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/* `spec`: 尾/公斤 */
/*
ALTER TABLE `ESP32`
ADD COLUMN `dispenser_ID` int(11) NOT NULL DEFAULT '1';
*/
--
-- Dumping data for table `ESP32`
--

LOCK TABLES `ESP32` WRITE;
/*!40000 ALTER TABLE `ESP32` DISABLE KEYS */;
INSERT INTO `ESP32` VALUES (22.46,0.00,'off','0','600','0','15:46:35','2023-10-05');
INSERT INTO `ESP32` VALUES (23.16,0.00,'off','0','600','0','15:46:40','2023-10-05');
INSERT INTO `ESP32` VALUES (23.27,0.00,'off','0','600','0','15:46:45','2023-10-05');
INSERT INTO `ESP32` VALUES (23.56,0.00,'off','0','600','0','15:46:50','2023-10-05');
INSERT INTO `ESP32` VALUES (23.57,0.00,'off','0','600','0','15:46:55','2023-10-05');

INSERT INTO `ESP32` VALUES (23.45,0.00,'off','0','600','0','15:47:00','2023-10-05');
INSERT INTO `ESP32` VALUES (23.52,0.00,'off','0','600','0','15:47:05','2023-10-05');
INSERT INTO `ESP32` VALUES (23.54,0.00,'off','0','600','0','15:47:10','2023-10-05');
INSERT INTO `ESP32` VALUES (24.98,0.00,'off','0','600','0','15:47:15','2023-10-05');
INSERT INTO `ESP32` VALUES (25.12,0.00,'off','0','600','0','15:47:20','2023-10-05');
INSERT INTO `ESP32` VALUES (26.32,0.00,'off','0','600','0','15:47:25','2023-10-05');
INSERT INTO `ESP32` VALUES (23.99,0.00,'off','0','600','0','15:47:30','2023-10-05');
INSERT INTO `ESP32` VALUES (24.18,0.00,'off','0','600','0','15:47:35','2023-10-05');
INSERT INTO `ESP32` VALUES (22.72,0.00,'off','0','600','0','15:47:40','2023-10-05');
INSERT INTO `ESP32` VALUES (22.52,0.00,'off','0','600','0','15:47:45','2023-10-05');
INSERT INTO `ESP32` VALUES (22.50,0.00,'off','0','600','0','15:47:50','2023-10-05');
INSERT INTO `ESP32` VALUES (22.68,0.00,'off','0','600','0','15:47:55','2023-10-05');

INSERT INTO `ESP32` VALUES (22.57,0.00,'off','0','600','0','15:48:00','2023-10-05');
INSERT INTO `ESP32` VALUES (22.56,0.00,'off','0','600','0','15:48:05','2023-10-05');
INSERT INTO `ESP32` VALUES (22.57,0.00,'off','0','600','0','15:48:10','2023-10-05');
INSERT INTO `ESP32` VALUES (22.57,0.00,'off','0','600','0','15:48:15','2023-10-05');
INSERT INTO `ESP32` VALUES (22.56,0.00,'off','0','600','0','15:48:20','2023-10-05');
INSERT INTO `ESP32` VALUES (22.56,0.00,'off','0','600','0','15:48:25','2023-10-05');
INSERT INTO `ESP32` VALUES (22.69,0.00,'off','0','600','0','15:48:30','2023-10-05');
INSERT INTO `ESP32` VALUES (22.66,0.00,'off','0','600','0','15:48:35','2023-10-05');
INSERT INTO `ESP32` VALUES (22.73,0.00,'off','0','600','0','15:48:40','2023-10-05');
INSERT INTO `ESP32` VALUES (22.53,0.00,'off','0','600','0','15:48:45','2023-10-05');
INSERT INTO `ESP32` VALUES (22.65,0.00,'off','0','600','0','15:48:50','2023-10-05');
INSERT INTO `ESP32` VALUES (22.71,0.00,'off','0','600','0','15:48:55','2023-10-05');
/*!40000 ALTER TABLE `ESP32` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feeding_logs`
--

DROP TABLE IF EXISTS `feeding_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `feeding_logs` (
  `pool_ID` int(11) DEFAULT NULL,
  `dispenser_ID` int(11) NOT NULL default '1',
  `start_time` datetime DEFAULT current_timestamp(),
  `use_time` float DEFAULT NULL,
  `food_ID` char(50) DEFAULT NULL,
  `feeding_amount` float DEFAULT NULL,
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feeding_logs`
--

LOCK TABLES `feeding_logs` WRITE;
/*!40000 ALTER TABLE `feeding_logs` DISABLE KEYS */;
INSERT INTO `feeding_logs` VALUES 
(1,'2023-04-01 13:00:00',30,'test',100000,1),
(2,'2023-04-02 13:00:00',30,'test',100000,1), 
(1,'2023-04-03 13:00:00',30,'test',100000,1),
(1,'2023-04-04 13:00:00',30,'test',100000,1),
(1,'2023-04-05 13:00:00',30,'test',100000,1),
(2,'2023-04-06 13:00:00',30,'test',100000,1), 
(1,'2023-04-07 13:00:00',30,'test',100000,1),
(1,'2023-04-08 13:00:00',30,'test',100000,1),
(2,'2023-04-09 13:00:00',30,'test',100000,1), 
(1,'2023-04-10 13:00:00',30,'test',100000,1);
/*!40000 ALTER TABLE `feeding_logs` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-04-09 11:00:33
