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
  `pool_ID` int(11) NOT NULL,
  `spec` float DEFAULT NULL,
  `record_weights` float DEFAULT NULL,
  `estimated_weights` float DEFAULT NULL,
  `fcr` varchar(255) DEFAULT '-',
  `dead_counts` int(11) DEFAULT NULL,
  `update_time` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
--
/* `spec`: 尾/公斤 */

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
-- Table structure for table `ESP32`
--
DROP TABLE IF EXISTS `ESP32`;
--
CREATE TABLE `ESP32` (
  `pool_ID` int(11) DEFAULT NULL,
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
--

--
-- Dumping data for table `ESP32`
--
LOCK TABLES `ESP32` WRITE;
--
INSERT INTO `ESP32` VALUES 
(1,1,22.46,0.00,'off','0','600','0','15:46:35','2023-10-05'), 
(1,1,23.16,0.00,'off','0','600','0','15:46:40','2023-10-05'), 

(1,1,23.27,0.00,'off','0','600','0','15:46:45','2023-10-05'),
(1,1,23.56,0.00,'off','0','600','0','15:46:50','2023-10-05'), 
(1,1,23.57,0.00,'off','0','600','0','15:46:55','2023-10-05'),
(1,1,23.45,0.00,'off','0','600','0','15:47:00','2023-10-05'),
(1,1,23.52,0.00,'off','0','600','0','15:47:05','2023-10-05'),
(1,1,23.54,0.00,'off','0','600','0','15:47:10','2023-10-05'),
(1,1,24.98,0.00,'off','0','600','0','15:47:15','2023-10-05'),
(1,1,25.12,0.00,'off','0','600','0','15:47:20','2023-10-05'),
(1,1,26.32,0.00,'off','0','600','0','15:47:25','2023-10-05'),
(1,1,23.99,0.00,'off','0','600','0','15:47:30','2023-10-05'),
(1,1,24.18,0.00,'off','0','600','0','15:47:35','2023-10-05'),
(1,1,22.72,0.00,'off','0','600','0','15:47:40','2023-10-05'),
(1,1,22.52,0.00,'off','0','600','0','15:47:45','2023-10-05'),
(1,1,22.50,0.00,'off','0','600','0','15:47:50','2023-10-05'),
(1,1,22.68,0.00,'off','0','600','0','15:47:55','2023-10-05'),

(1,1,22.57,0.00,'off','0','600','0','15:48:00','2023-10-05'),
(1,1,22.56,0.00,'off','0','600','0','15:48:05','2023-10-05'),
(1,1,22.57,0.00,'off','0','600','0','15:48:10','2023-10-05'),
(1,1,22.57,0.00,'off','0','600','0','15:48:15','2023-10-05'),
(1,1,22.56,0.00,'off','0','600','0','15:48:20','2023-10-05'),
(1,1,22.56,0.00,'off','0','600','0','15:48:25','2023-10-05'),
(1,1,22.69,0.00,'off','0','600','0','15:48:30','2023-10-05'),
(1,1,22.66,0.00,'off','0','600','0','15:48:35','2023-10-05'),
(1,1,22.73,0.00,'off','0','600','0','15:48:40','2023-10-05'),
(1,1,22.53,0.00,'off','0','600','0','15:48:45','2023-10-05'),
(1,1,22.65,0.00,'off','0','600','0','15:48:50','2023-10-05'),
(1,1,22.71,0.00,'off','0','600','0','15:48:55','2023-10-05'),

(1,1,22.66,0.00,'off','0','600','0','17:00:00','2023-10-06'),
(1,1,25.00,0.00,'off','0','600','0','17:17:17','2023-10-07');
--
UNLOCK TABLES;

--
-- Table structure for table `feeding_logs`
--
UPDATE feeding_logs SET pool_ID = 1 WHERE dispenser_ID = 1;

DROP TABLE IF EXISTS `feeding_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `feeding_logs` (
  `pool_ID` int(11) DEFAULT NULL,
  `dispenser_ID` int(11) NOT NULL default '1',
  `start_time` datetime DEFAULT current_timestamp(),
  `use_time` float DEFAULT NULL,
  `food_ID` varchar(255) DEFAULT NULL,
  `feeding_amount` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
--

--
-- Dumping data for table `feeding_logs`
--
LOCK TABLES `feeding_logs` WRITE;
--
INSERT INTO `feeding_logs` VALUES 
(6, 1,'2023-10-01 12:50:00',60, NULL,10),
(6, 1,'2023-10-02 13:24:00',60, NULL,10),
(6, 1,'2023-10-03 14:00:00',60, NULL,10),
(6, 1,'2023-10-04 11:45:00',60, NULL,10),
(6, 1,'2023-10-05 11:57:00',60, NULL,10),
(6, 1,'2023-10-06 12:23:00',60, NULL,10),
(6, 1,'2023-10-07 12:36:00',60, NULL,10),
(6, 1,'2023-10-08 13:04:00',60, NULL,10),
(6, 1,'2023-10-09 13:00:00',60, NULL,10),
(6, 1,'2023-10-10 10:37:00',60, NULL,10),

(6, 1,'2023-10-11 10:37:00',60, NULL,11),
(6, 1,'2023-10-12 12:36:00',60, NULL,11),
(6, 1,'2023-10-13 13:04:00',60, NULL,11),
(6, 1,'2023-10-14 11:57:00',60, NULL,11),
(6, 1,'2023-10-15 10:37:00',60, NULL,11),
(6, 1,'2023-10-16 12:36:00',60, NULL,11),
(6, 1,'2023-10-17 11:57:00',60, NULL,11),
(6, 1,'2023-10-18 11:45:00',60, NULL,11),
(6, 1,'2023-10-19 13:04:00',60, NULL,11),
(6, 1,'2023-10-20 10:37:00',60, NULL,11),

(6, 1,'2023-10-21 12:36:00',60, NULL,12),
(6, 1,'2023-10-22 11:57:00',60, NULL,12),
(6, 1,'2023-10-23 13:50:00',60, NULL,12),
(6, 1,'2023-10-24 12:50:00',60, NULL,12),
(6, 1,'2023-10-25 13:04:00',60, NULL,12),
(6, 1,'2023-10-26 10:37:00',60, NULL,12),
(6, 1,'2023-10-27 11:45:00',60, NULL,12),
(6, 1,'2023-10-28 11:57:00',60, NULL,12),
(6, 1,'2023-10-29 13:50:00',60, NULL,12),
(6, 1,'2023-10-30 12:50:00',60, NULL,12);
--
UNLOCK TABLES;
--
UPDATE feeding_logs SET food_ID='2號料' WHERE food_ID='test';
--
UPDATE feeding_logs SET food_ID='鱸魚3號';
UPDATE feeding_logs SET feeding_amount='170.5' WHERE start_time = '2023-10-25 13:04:00';

--
-- Table structure for table `decision`
--
DROP TABLE IF EXISTS `decision`;
-- 
CREATE TABLE `decision` (
  `id` varchar(1) NOT NULL PRIMARY KEY,
  `mode` varchar(1) DEFAULT NULL,
  `angle` varchar(3) DEFAULT NULL,
  `period` varchar(3) DEFAULT NULL,
  `amount` varchar(3) DEFAULT NULL,
  `fetch_interval` varchar(3) DEFAULT NULL
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
--

--
-- Table structure for table `frames`
--
DROP TABLE IF EXISTS `frames`;
-- 
CREATE TABLE `frames` (
    `id` INT(11) NOT NULL PRIMARY KEY,
    `name` VARCHAR(255) DEFAULT NULL,
    `update_time` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
    `data` LONGBLOB DEFAULT NULL
);

+-------+--------------+------+-----+---------+-------+
| Field | Type         | Null | Key | Default | Extra |
+-------+--------------+------+-----+---------+-------+
| id    | int(11)      | NO   | PRI | NULL    |       |
| name  | varchar(255) | YES  |     | NULL    |       |
| data  | longblob     | YES  |     | NULL    |       |
+-------+--------------+------+-----+---------+-------+

CREATE TABLE feeding_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    aquarium_id INT,
    journal_id INT,
    action VARCHAR(255),
    date BIGINT,
    food_id INT,
    food_weight INT,
    food_unit VARCHAR(255),
    food_name VARCHAR(255),
    feeding_time BIGINT,
    period INT,
    status VARCHAR(255),
    left_amount VARCHAR(255),
    description TEXT,
    checked_list VARCHAR(255),
    name VARCHAR(255),
    version INT
);

INSERT INTO feeding_records (
    aquarium_id,
    journal_id,
    action,
    date,
    food_id,
    food_weight,
    food_unit,
    food_name,
    feeding_time,
    period,
    status,
    left_amount,
    description,
    checked_list,
    name,
    version
) VALUES (
    '84',
    '0',
    'create',
    '1693877576891',
    '19',
    '5',
    'catty',
    'A牌',
    '1693877520000',
    '35',
    'normal',
    '',
    '吃很久',
    '19',
    'configure_journal_feeding',
    '1'
);

ERROR 1366 (HY000): Incorrect string value, 資料庫字符集和校對(collation)不支援存儲這個特定的 Unicode 字符
solution
更改資料庫字符集和校對: 將字符集設定為 'utf8mb4'，並選擇一個適當的校對，如 'utf8mb4_unicode_ci'
ALTER DATABASE your_database_name CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
更改表格的字符集和校對
ALTER TABLE your_table_name CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


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

-- 複製 feeding_logs 表格結構
CREATE TABLE ar0DB.feeding_logs LIKE fishDB.feeding_logs;

-- 複製 feeding_records 表格結構
CREATE TABLE ar0DB.feeding_records LIKE fishDB.feeding_records;

-- 複製 field_logs 表格結構
CREATE TABLE ar0DB.field_logs LIKE fishDB.field_logs;

-- 複製 ripple_frames 表格結構
CREATE TABLE ar0DB.ripple_frames LIKE fishDB.ripple_frames;
