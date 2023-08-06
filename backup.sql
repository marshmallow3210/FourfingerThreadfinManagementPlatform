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
-- Table structure for table `feed_conversion`
--

DROP TABLE IF EXISTS `feed_conversion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `feed_conversion` (
  `field_ID` int(11) DEFAULT NULL,
  `feed_conversion` float DEFAULT NULL,
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feed_conversion`
--

LOCK TABLES `feed_conversion` WRITE;
/*!40000 ALTER TABLE `feed_conversion` DISABLE KEYS */;
INSERT INTO `feed_conversion` VALUES (1,2,'2023-03-12 11:13:42','2023-03-12 11:15:48');
/*!40000 ALTER TABLE `feed_conversion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feeding_fields`
--

DROP TABLE IF EXISTS `feeding_fields`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `feeding_fields` (
  `field_ID` int(11) NOT NULL,
  `spec` int(11) DEFAULT NULL,
  `weights` float DEFAULT NULL,
  `estimated_weights` float DEFAULT NULL,
  `feed_conversion` float DEFAULT NULL,
  `dead_counts` int(11) DEFAULT NULL,
  `update_time` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/* `spec`: 尾/公斤 */
--
-- Dumping data for table `feeding_fields`
--

LOCK TABLES `feeding_fields` WRITE;
/*!40000 ALTER TABLE `feeding_fields` DISABLE KEYS */;
INSERT INTO `feeding_fields` VALUES (1,100,300,300,0,0,'2023-03-01 12:30:00'),(1,50,600,600,2,100,'2023-04-01 12:30:00');
INSERT INTO `feeding_fields` VALUES (2,120,300,300,0,0,'2023-03-01 12:30:00'),(2,90,400,400,2,100,'2023-03-10 12:30:00'),(2,60,600,600,2,100,'2023-04-01 12:30:00');
/*!40000 ALTER TABLE `feeding_fields` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feeding_logs`
--

DROP TABLE IF EXISTS `feeding_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `feeding_logs` (
  `dispenser_ID` int(11) DEFAULT NULL,
  `feeding_time` datetime DEFAULT current_timestamp(),
  `use_time` float DEFAULT NULL,
  `food_ID` char(50) DEFAULT NULL,
  `used` float DEFAULT NULL,
  `field_ID` int(11) DEFAULT NULL
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
