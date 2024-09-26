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
-- Table structure for table `field_logs`
--
DROP TABLE IF EXISTS `field_logs`;
--
CREATE TABLE `field_logs` (
  `pool_id` int(11) NOT NULL,
  `spec` float DEFAULT NULL,
  `record_weights` float DEFAULT NULL,
  `estimated_weights` float DEFAULT NULL,
  `fcr` varchar(255) DEFAULT '-',
  `dead_counts` int(11) DEFAULT NULL,
  `update_time` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
--
/* `spec`: 尾/斤 */
/* `record_weights`:斤 */
/* `estimated_weights`:斤 */

--
-- Dumping data for table `field_logs`
--
LOCK TABLES `field_logs` WRITE;
--
INSERT INTO `field_logs` VALUES (1,100.0,300.0,300.0,'-',0,'2023-03-01 12:30:00'),(1,50.0,600.0,600.0,'-',0,'2023-04-01 12:30:00');
INSERT INTO `field_logs` VALUES (2,120.0,300.0,300.0,'-',0,'2023-03-02 12:00:00'),(2,90.0,400.0,400.0,'-',0,'2023-03-10 12:20:00'),(2,60.0,600.0,600.0,'-',0,'2023-04-01 12:40:00');
INSERT INTO `field_logs` VALUES (3,145.0,500.0,500.0,'-',0,'2023-03-03 12:45:00'),(3,98.0,850.0,900.0,'-',0,'2023-04-04 12:00:00');
--
UNLOCK TABLES;

UPDATE field_logs SET fcr='-';

--
-- Table structure for table `feeding_logs`
--
UPDATE feeding_logs SET pool_id = 1 WHERE dispenser_id = 1;

DROP TABLE IF EXISTS `new_feeding_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `new_feeding_logs` (
  `journal_id` int(11) NOT NULL default '1',
  `pool_id` int(11) NOT NULL default '1',
  `dispenser_id` int(11) NOT NULL default '1',
  `start_time` datetime DEFAULT current_timestamp(),
  `use_time` float DEFAULT NULL,
  `food_id` int(11) DEFAULT NULL,
  `food_name` varchar(255) DEFAULT NULL,
  `food_unit` varchar(255) DEFAULT 'kg',
  `feeding_amount` float DEFAULT NULL,
  `left_amount` float DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
--
ALTER TABLE new_feeding_logs ADD COLUMN recommended_feeding_amount FLOAT DEFAULT NULL AFTER feeding_amount;

--
-- Dumping data for table `feeding_logs`
--
LOCK TABLES `feeding_logs` WRITE;
--
INSERT INTO `new_feeding_logs` VALUES 
(1, 1, 1, '2024-04-29 06:42:00', 45, 1, '1號料', 'kg', 500, 20000, 'normal', '測試測試'),
(2, 1, 1, '2024-04-29 08:04:00', 120, 1, '1號料', 'kg', 1600, 18400, 'normal', '測試測試'),
(3, 1, 1, '2024-04-29 11:54:00', 72, 1, '1號料', 'kg', 950, 17450, 'good', '測試測試'),
(4, 1, 1, '2024-04-29 14:01:00', 100, 1, '1號料', 'kg', 1435, 16015, 'normal', '測試測試'),
(5, 1, 1, '2024-04-29 17:13:00', 108, 1, '1號料', 'kg', 960, 15055, 'bad', '測試測試'),
(6, 1, 1, '2024-04-30 06:20:00', 30, 2, '2號料', 'kg', 450, 20050, 'normal', '測試測試'),
(7, 1, 1, '2024-04-30 07:14:00', 76, 2, '2號料', 'kg', 960, 19090, 'good', '測試測試'),
(8, 1, 1, '2024-04-30 08:45:00', 140, 2, '2號料', 'kg', 1865, 17225, 'good', '測試測試'),
(9, 1, 1, '2024-04-30 12:00:00', 85, 2, '2號料', 'kg', 1125, 16100, 'good', '測試測試'),
(10, 1, 1, '2024-04-30 14:14:00', 48, 2, '2號料', 'kg', 560, 15540, 'normal', '測試測試');

INSERT INTO `new_feeding_logs` VALUES 
(1, 1, 1, '2024-05-01 06:42:00', 45, 1, '1號料', 'kg', 500, 20000, 'normal', '測試測試'),
(2, 1, 1, '2024-05-01 08:04:00', 120, 1, '1號料', 'kg', 1600, 18400, 'normal', '測試測試'),
(3, 1, 1, '2024-05-01 11:54:00', 72, 1, '1號料', 'kg', 950, 17450, 'good', '測試測試'),
(4, 1, 1, '2024-05-01 14:01:00', 100, 1, '1號料', 'kg', 1435, 16015, 'normal', '測試測試'),
(5, 1, 1, '2024-05-01 17:13:00', 108, 1, '1號料', 'kg', 960, 15055, 'bad', '測試測試'),
(6, 1, 1, '2024-05-02 06:20:00', 30, 2, '2號料', 'kg', 450, 20050, 'normal', '測試測試'),
(7, 1, 1, '2024-05-02 07:14:00', 76, 2, '2號料', 'kg', 960, 19090, 'good', '測試測試'),
(8, 1, 1, '2024-05-02 08:45:00', 140, 2, '2號料', 'kg', 1865, 17225, 'good', '測試測試'),
(9, 1, 1, '2024-05-02 12:00:00', 85, 2, '2號料', 'kg', 1125, 16100, 'good', '測試測試'),
(10, 1, 1, '2024-05-02 14:14:00', 48, 2, '2號料', 'kg', 560, 15540, 'normal', '測試測試');
--
UNLOCK TABLES;
--
UPDATE feeding_logs SET food_ID='2號料' WHERE food_ID='test';
--
UPDATE feeding_logs SET food_ID='鱸魚3號';
UPDATE feeding_logs SET feeding_amount='170.5' WHERE start_time = '2023-10-25 13:04:00';

--
-- Table structure for table `ripple_frames`
--
DROP TABLE IF EXISTS `ripple_frames`;
-- 
CREATE TABLE `ripple_frames` (
    `id` INT(11) NOT NULL PRIMARY KEY,
    `frame_data` LONGBLOB DEFAULT NULL,
    `value` INT(11) DEFAULT 0,
    `isChoose` TINYINT(1) DEFAULT 0
);


-- tables of database to copy: 
-- feeding_logs, feeding_records, field_logs, ripple_frames

-- 複製表格結構
CREATE TABLE ar0DB.feeding_logs LIKE fishDB.feeding_logs;
CREATE TABLE ar0DB.feeding_records LIKE fishDB.feeding_records;
CREATE TABLE ar0DB.field_logs LIKE fishDB.field_logs;
CREATE TABLE ar0DB.ripple_frames LIKE fishDB.ripple_frames;

update decision set mode=1;

SELECT * FROM ESP32 ORDER BY CONCAT(date, ' ', time) DESC LIMIT 5;
delete FROM ESP32 ORDER BY CONCAT(date, ' ', time) DESC LIMIT 5;

select * from feeding_logs order by start_time desc limit 5;

SELECT blower_state FROM fishDB.ESP32 ORDER BY CONCAT(date, ' ', time) DESC LIMIT 1;
UPDATE fishDB.ESP32 SET blower_state = 'off' ORDER BY CONCAT(date, ' ', time) DESC LIMIT 1;

UPDATE new_feeding_logs 
SET description = 
    CASE 
        WHEN description IS NULL OR description = '' 
        THEN '調機階段' 
        ELSE CONCAT(description, ', 調機階段') 
    END
WHERE feeding_amount < 30;
