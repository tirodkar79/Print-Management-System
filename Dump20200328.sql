-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: printer_logs
-- ------------------------------------------------------
-- Server version	8.0.19

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES ('Admin','Admin');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `daily`
--

DROP TABLE IF EXISTS `daily`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `daily` (
  `grp_id` varchar(20) NOT NULL,
  `monday` int DEFAULT NULL,
  `tuesday` int DEFAULT NULL,
  `wednesday` int DEFAULT NULL,
  `thursday` int DEFAULT NULL,
  `friday` int DEFAULT NULL,
  `week` int DEFAULT NULL,
  PRIMARY KEY (`grp_id`),
  CONSTRAINT `daily_ibfk_1` FOREIGN KEY (`grp_id`) REFERENCES `students` (`grp_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `daily`
--

LOCK TABLES `daily` WRITE;
/*!40000 ALTER TABLE `daily` DISABLE KEYS */;
INSERT INTO `daily` VALUES ('TE06_0101',0,0,0,0,0,0),('TE06_0102',0,0,0,0,0,0),('TE06_0103',0,0,0,0,0,0);
/*!40000 ALTER TABLE `daily` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students` (
  `grp_id` varchar(20) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `second_name` varchar(30) NOT NULL,
  `third_name` varchar(30) NOT NULL,
  `roll_1` int NOT NULL,
  `roll_2` int NOT NULL,
  `roll_3` int NOT NULL,
  `year` varchar(10) NOT NULL,
  `sem` int DEFAULT NULL,
  `batch` int NOT NULL,
  `password` varchar(20) NOT NULL,
  `reg_date` datetime NOT NULL DEFAULT '2020-03-23 11:47:00',
  PRIMARY KEY (`grp_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
INSERT INTO `students` VALUES ('TE06_0101','Prathmesh Tirodkar','Harshali Malgundkar','Saurabh Maurya',18,17,16,'TE',6,1,'Prathmesh@15','2020-03-23 11:56:25'),('TE06_0102','Neeraj Guhagar','Sanjana Desai','Swanand Vaishawmpa',1,2,3,'TE',6,1,'Neeraj@30','2020-03-27 18:37:18'),('TE06_0103','Shubham Warang','Sneha Kamble','Rutika Naik',15,14,13,'TE',6,1,'Arjun@12','2020-03-27 23:16:49');
/*!40000 ALTER TABLE `students` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `week`
--

DROP TABLE IF EXISTS `week`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `week` (
  `grp_id` varchar(20) NOT NULL,
  `week1` int DEFAULT NULL,
  `week2` int DEFAULT NULL,
  `week3` int DEFAULT NULL,
  `week4` int DEFAULT NULL,
  `week5` int DEFAULT NULL,
  `week6` int DEFAULT NULL,
  `week7` int DEFAULT NULL,
  `week8` int DEFAULT NULL,
  `week9` int DEFAULT NULL,
  `week10` int DEFAULT NULL,
  `week11` int DEFAULT NULL,
  `week12` int DEFAULT NULL,
  `week13` int DEFAULT NULL,
  `week14` int DEFAULT NULL,
  `week15` int DEFAULT NULL,
  PRIMARY KEY (`grp_id`),
  CONSTRAINT `week_ibfk_1` FOREIGN KEY (`grp_id`) REFERENCES `students` (`grp_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `week`
--

LOCK TABLES `week` WRITE;
/*!40000 ALTER TABLE `week` DISABLE KEYS */;
INSERT INTO `week` VALUES ('TE06_0101',3,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('TE06_0102',5,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('TE06_0103',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
/*!40000 ALTER TABLE `week` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'printer_logs'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-03-28  0:05:42
