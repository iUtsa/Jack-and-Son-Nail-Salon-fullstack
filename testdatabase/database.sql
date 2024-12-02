CREATE DATABASE  IF NOT EXISTS `test1` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `test1`;
-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: test1
-- ------------------------------------------------------
-- Server version	8.0.40

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
-- Table structure for table `appointments`
--

DROP TABLE IF EXISTS `appointments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appointments` (
  `appt_id` int NOT NULL AUTO_INCREMENT,
  `booking_number` varchar(50) DEFAULT NULL,
  `customer_id` int DEFAULT NULL,
  `service_id` int DEFAULT NULL,
  `appointment_date` date DEFAULT NULL,
  `appointment_start_time` time DEFAULT NULL,
  `appointment_end_time` time DEFAULT NULL,
  PRIMARY KEY (`appt_id`),
  KEY `customer_id` (`customer_id`),
  KEY `service_id` (`service_id`),
  CONSTRAINT `appointments_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `users` (`CustomerID`),
  CONSTRAINT `appointments_ibfk_2` FOREIGN KEY (`service_id`) REFERENCES `services` (`service_id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appointments`
--

LOCK TABLES `appointments` WRITE;
/*!40000 ALTER TABLE `appointments` DISABLE KEYS */;
INSERT INTO `appointments` VALUES (11,'BK19285',3,19,'2024-11-09','21:52:00','22:22:00'),(12,'BK512354',3,16,'2024-11-07','08:00:00','08:30:00'),(13,'BK314790',7,15,'2024-11-08','23:17:00','23:47:00'),(14,'BK964722',7,31,'2024-11-09','23:17:00','23:47:00'),(15,'BK333940',7,6,'2024-11-13','23:17:00','23:47:00'),(16,'BK333940',7,6,'2024-11-13','17:30:00','18:00:00'),(17,'BK333940',7,6,'2024-11-30','17:30:00','18:00:00');
/*!40000 ALTER TABLE `appointments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `business_hours`
--

DROP TABLE IF EXISTS `business_hours`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `business_hours` (
  `id` int NOT NULL AUTO_INCREMENT,
  `day` enum('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday') NOT NULL,
  `open_hour` time NOT NULL,
  `close_hour` time NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `business_hours`
--

LOCK TABLES `business_hours` WRITE;
/*!40000 ALTER TABLE `business_hours` DISABLE KEYS */;
INSERT INTO `business_hours` VALUES (8,'Monday','14:30:00','17:00:00'),(9,'Tuesday','05:36:00','19:00:00'),(10,'Wednesday','09:00:00','19:00:00'),(11,'Thursday','09:00:00','19:00:00'),(12,'Friday','09:00:00','19:00:00'),(13,'Saturday','09:00:00','19:00:00'),(14,'Sunday','00:00:00','00:00:00');
/*!40000 ALTER TABLE `business_hours` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee`
--

DROP TABLE IF EXISTS `employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee` (
  `EmployeeID` int NOT NULL AUTO_INCREMENT,
  `Employee_name` varchar(50) NOT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `Phone` varchar(15) NOT NULL,
  `services_provided` varchar(100) NOT NULL,
  PRIMARY KEY (`EmployeeID`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee`
--

LOCK TABLES `employee` WRITE;
/*!40000 ALTER TABLE `employee` DISABLE KEYS */;
INSERT INTO `employee` VALUES (1,'Alice Johnson','alice.johnson@example.com','123-456-1312','Nail Care, Manicure, Pedicure, Waxing'),(2,'Bob Smith','bob.smith@example.com','234-567-8901','Pedidcure, Manicure'),(3,'Cathy Brown','cathy.brown@example.com','345-678-9012','Nail Care'),(4,'David Lee','david.lee@example.com','456-789-0123','Waxing, Nail Care'),(5,'Emily Davis','emily.davis@example.com','567-890-1234','Waxing, Nail Care'),(6,'Franklin Reed','franklin.reed@example.com','678-901-2345','Nail Care, Manicure'),(7,'Grace Kim','grace.kim@example.com','789-012-3456','Nail Care, Pedicure'),(8,'Henry Adams','henry.adams@example.com','890-123-4567','Manicure'),(9,'Irene White','irene.white@example.com','901-234-5678','Pedicure, Manicure'),(10,'Jack Wilson','jack.wilson@example.com','012-345-6789','Haircut'),(12,'Jackson Pham','jack.pham2024@gmail.com','609-209-1920','Nail Care, Manicure, Pedicure');
/*!40000 ALTER TABLE `employee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee_schedule`
--

DROP TABLE IF EXISTS `employee_schedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee_schedule` (
  `schedule_id` int NOT NULL AUTO_INCREMENT,
  `employee_id` int DEFAULT NULL,
  `day_of_week` enum('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday') NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  PRIMARY KEY (`schedule_id`),
  KEY `employee_id` (`employee_id`),
  CONSTRAINT `employee_schedule_ibfk_1` FOREIGN KEY (`employee_id`) REFERENCES `users` (`CustomerID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee_schedule`
--

LOCK TABLES `employee_schedule` WRITE;
/*!40000 ALTER TABLE `employee_schedule` DISABLE KEYS */;
/*!40000 ALTER TABLE `employee_schedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `manager_schedule`
--

DROP TABLE IF EXISTS `manager_schedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `manager_schedule` (
  `id` int NOT NULL AUTO_INCREMENT,
  `managerID` int NOT NULL,
  `time_slot` time NOT NULL,
  `day_of_week` varchar(20) NOT NULL,
  `comment` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `managerID` (`managerID`),
  CONSTRAINT `manager_schedule_ibfk_1` FOREIGN KEY (`managerID`) REFERENCES `managers` (`managerID`)
) ENGINE=InnoDB AUTO_INCREMENT=169 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `manager_schedule`
--

LOCK TABLES `manager_schedule` WRITE;
/*!40000 ALTER TABLE `manager_schedule` DISABLE KEYS */;
INSERT INTO `manager_schedule` VALUES (1,101123,'08:00:00','Monday',''),(2,101123,'09:00:00','Monday',''),(3,101123,'10:00:00','Monday',''),(4,101123,'11:00:00','Monday',''),(5,101123,'12:00:00','Monday',''),(6,101123,'13:00:00','Monday',''),(7,101123,'14:00:00','Monday',''),(8,101123,'15:00:00','Monday',''),(9,101123,'16:00:00','Monday',''),(10,101123,'17:00:00','Monday',''),(11,101123,'18:00:00','Monday',''),(12,101123,'19:00:00','Monday',''),(13,101123,'08:00:00','Tuesday',''),(14,101123,'09:00:00','Tuesday',''),(15,101123,'10:00:00','Tuesday',''),(16,101123,'11:00:00','Tuesday',''),(17,101123,'12:00:00','Tuesday',''),(18,101123,'13:00:00','Tuesday',''),(19,101123,'14:00:00','Tuesday',''),(20,101123,'15:00:00','Tuesday',''),(21,101123,'16:00:00','Tuesday',''),(22,101123,'17:00:00','Tuesday',''),(23,101123,'18:00:00','Tuesday',''),(24,101123,'19:00:00','Tuesday',''),(25,101123,'08:00:00','Wednesday',''),(26,101123,'09:00:00','Wednesday',''),(27,101123,'10:00:00','Wednesday',''),(28,101123,'11:00:00','Wednesday',''),(29,101123,'12:00:00','Wednesday',''),(30,101123,'13:00:00','Wednesday',''),(31,101123,'14:00:00','Wednesday',''),(32,101123,'15:00:00','Wednesday',''),(33,101123,'16:00:00','Wednesday',''),(34,101123,'17:00:00','Wednesday',''),(35,101123,'18:00:00','Wednesday',''),(36,101123,'19:00:00','Wednesday',''),(37,101123,'08:00:00','Thursday',''),(38,101123,'09:00:00','Thursday',''),(39,101123,'10:00:00','Thursday',''),(40,101123,'11:00:00','Thursday',''),(41,101123,'12:00:00','Thursday',''),(42,101123,'13:00:00','Thursday',''),(43,101123,'14:00:00','Thursday',''),(44,101123,'15:00:00','Thursday',''),(45,101123,'16:00:00','Thursday',''),(46,101123,'17:00:00','Thursday',''),(47,101123,'18:00:00','Thursday',''),(48,101123,'19:00:00','Thursday',''),(49,101123,'08:00:00','Friday',''),(50,101123,'09:00:00','Friday',''),(51,101123,'10:00:00','Friday',''),(52,101123,'11:00:00','Friday',''),(53,101123,'12:00:00','Friday',''),(54,101123,'13:00:00','Friday',''),(55,101123,'14:00:00','Friday',''),(56,101123,'15:00:00','Friday',''),(57,101123,'16:00:00','Friday',''),(58,101123,'17:00:00','Friday',''),(59,101123,'18:00:00','Friday',''),(60,101123,'19:00:00','Friday',''),(61,101123,'08:00:00','Saturday',''),(62,101123,'09:00:00','Saturday',''),(63,101123,'10:00:00','Saturday',''),(64,101123,'11:00:00','Saturday',''),(65,101123,'12:00:00','Saturday',''),(66,101123,'13:00:00','Saturday',''),(67,101123,'14:00:00','Saturday',''),(68,101123,'15:00:00','Saturday',''),(69,101123,'16:00:00','Saturday',''),(70,101123,'17:00:00','Saturday',''),(71,101123,'18:00:00','Saturday',''),(72,101123,'19:00:00','Saturday',''),(73,101123,'08:00:00','Sunday',''),(74,101123,'09:00:00','Sunday',''),(75,101123,'10:00:00','Sunday',''),(76,101123,'11:00:00','Sunday',''),(77,101123,'12:00:00','Sunday',''),(78,101123,'13:00:00','Sunday',''),(79,101123,'14:00:00','Sunday',''),(80,101123,'15:00:00','Sunday',''),(81,101123,'16:00:00','Sunday',''),(82,101123,'17:00:00','Sunday',''),(83,101123,'18:00:00','Sunday',''),(84,101123,'19:00:00','Sunday',''),(85,101123,'08:00:00','Monday',''),(86,101123,'09:00:00','Monday',''),(87,101123,'10:00:00','Monday',''),(88,101123,'11:00:00','Monday',''),(89,101123,'12:00:00','Monday',''),(90,101123,'13:00:00','Monday',''),(91,101123,'14:00:00','Monday',''),(92,101123,'15:00:00','Monday',''),(93,101123,'16:00:00','Monday',''),(94,101123,'17:00:00','Monday',''),(95,101123,'18:00:00','Monday',''),(96,101123,'19:00:00','Monday',''),(97,101123,'08:00:00','Tuesday',''),(98,101123,'09:00:00','Tuesday',''),(99,101123,'10:00:00','Tuesday',''),(100,101123,'11:00:00','Tuesday',''),(101,101123,'12:00:00','Tuesday',''),(102,101123,'13:00:00','Tuesday',''),(103,101123,'14:00:00','Tuesday',''),(104,101123,'15:00:00','Tuesday',''),(105,101123,'16:00:00','Tuesday',''),(106,101123,'17:00:00','Tuesday',''),(107,101123,'18:00:00','Tuesday',''),(108,101123,'19:00:00','Tuesday',''),(109,101123,'08:00:00','Wednesday',''),(110,101123,'09:00:00','Wednesday',''),(111,101123,'10:00:00','Wednesday',''),(112,101123,'11:00:00','Wednesday',''),(113,101123,'12:00:00','Wednesday',''),(114,101123,'13:00:00','Wednesday',''),(115,101123,'14:00:00','Wednesday',''),(116,101123,'15:00:00','Wednesday',''),(117,101123,'16:00:00','Wednesday',''),(118,101123,'17:00:00','Wednesday',''),(119,101123,'18:00:00','Wednesday',''),(120,101123,'19:00:00','Wednesday',''),(121,101123,'08:00:00','Thursday',''),(122,101123,'09:00:00','Thursday',''),(123,101123,'10:00:00','Thursday',''),(124,101123,'11:00:00','Thursday',''),(125,101123,'12:00:00','Thursday',''),(126,101123,'13:00:00','Thursday',''),(127,101123,'14:00:00','Thursday',''),(128,101123,'15:00:00','Thursday',''),(129,101123,'16:00:00','Thursday',''),(130,101123,'17:00:00','Thursday',''),(131,101123,'18:00:00','Thursday',''),(132,101123,'19:00:00','Thursday',''),(133,101123,'08:00:00','Friday',''),(134,101123,'09:00:00','Friday',''),(135,101123,'10:00:00','Friday',''),(136,101123,'11:00:00','Friday',''),(137,101123,'12:00:00','Friday',''),(138,101123,'13:00:00','Friday',''),(139,101123,'14:00:00','Friday',''),(140,101123,'15:00:00','Friday',''),(141,101123,'16:00:00','Friday',''),(142,101123,'17:00:00','Friday',''),(143,101123,'18:00:00','Friday',''),(144,101123,'19:00:00','Friday',''),(145,101123,'08:00:00','Saturday',''),(146,101123,'09:00:00','Saturday',''),(147,101123,'10:00:00','Saturday',''),(148,101123,'11:00:00','Saturday',''),(149,101123,'12:00:00','Saturday',''),(150,101123,'13:00:00','Saturday',''),(151,101123,'14:00:00','Saturday',''),(152,101123,'15:00:00','Saturday',''),(153,101123,'16:00:00','Saturday',''),(154,101123,'17:00:00','Saturday',''),(155,101123,'18:00:00','Saturday',''),(156,101123,'19:00:00','Saturday',''),(157,101123,'08:00:00','Sunday',''),(158,101123,'09:00:00','Sunday',''),(159,101123,'10:00:00','Sunday',''),(160,101123,'11:00:00','Sunday',''),(161,101123,'12:00:00','Sunday',''),(162,101123,'13:00:00','Sunday',''),(163,101123,'14:00:00','Sunday',''),(164,101123,'15:00:00','Sunday',''),(165,101123,'16:00:00','Sunday',''),(166,101123,'17:00:00','Sunday',''),(167,101123,'18:00:00','Sunday',''),(168,101123,'19:00:00','Sunday','');
/*!40000 ALTER TABLE `manager_schedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `managers`
--

DROP TABLE IF EXISTS `managers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `managers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `managerID` int NOT NULL,
  `UserName` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `Name` varchar(50) DEFAULT NULL,
  `phone` varchar(11) NOT NULL,
  `email` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `managerID` (`managerID`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `managers`
--

LOCK TABLES `managers` WRITE;
/*!40000 ALTER TABLE `managers` DISABLE KEYS */;
INSERT INTO `managers` VALUES (1,101123,'tinaPham','scrypt:32768:8:1$ZGKc2gpxyBpJiVBh$ffefad81869a2d84d05942da4f8a0d0f0f323fed393298cd67f2f89290507829daa68309af7b97b240ced1311c6af96b316e6ec2d25a73f2d1072ff6758fd25d','Tina Pham','6098889898','managerTina@gmail.com'),(9,101101,'t2024','scrypt:32768:8:1$dNGko36u2NUEyimn$0e94f409a2fde00248aa80653587091dae31b3dd0cf29d15c4649eab218694d4ff381cdead7527dc213daa480e1f8e69007275655afd1f41b852364499cfc6ff','Thinh Tran','13123132','t2024@gmail.com');
/*!40000 ALTER TABLE `managers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `services`
--

DROP TABLE IF EXISTS `services`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `services` (
  `service_id` int NOT NULL AUTO_INCREMENT,
  `service_type` varchar(50) NOT NULL,
  `service_name` varchar(100) NOT NULL,
  `image` varchar(50) NOT NULL,
  `price` varchar(20) NOT NULL,
  PRIMARY KEY (`service_id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `services`
--

LOCK TABLES `services` WRITE;
/*!40000 ALTER TABLE `services` DISABLE KEYS */;
INSERT INTO `services` VALUES (1,'nailcare','Pink & White Full Set','/static/photos/nc1final.jpg','$60.00'),(2,'nailcare','Pink & White Fill In','/static/photos/nc2.jpg','$50.00'),(3,'nailcare','Acrylic Full Set','/static/photos/nc3.jpg','$1231.00'),(4,'nailcare','Acrylic Fill In','/static/photos/nc4.jpg','$40.00'),(5,'nailcare','Gel Color Full Set','/static/photos/nc5.jpg','$50.00'),(6,'nailcare','Gel Color Fill In','/static/photos/nc6.jpg','$40.00'),(7,'nailcare','Dipping Powder','/static/photos/nc7.jpg','$50.00+'),(8,'nailcare','UV Gel Full Set','/static/photos/nc8.jpg','$60.00'),(9,'nailcare','UV Gel Fill In','/static/photos/nc9.jpg','$45.00'),(10,'nailcare','Nail Repair','/static/photos/nc10.jpg','$5.00+'),(11,'nailcare','Cut Down Designs','/static/photos/nc11.jpg','$5.00+'),(12,'manicure','Pedicure & Manicure','/static/photos/mani1.jpg','$50.00'),(13,'manicure','Regular Pedicure','/static/photos/mani2.jpg','$30.00'),(14,'manicure','Regular Manicure','/static/photos/mani3.jpg','$20.00'),(15,'manicure','Gel Manicure','/static/photos/mani4.jpg','$35.00'),(16,'manicure','Deluxe Manicure','/static/photos/mani5.jpg','$30.00'),(17,'manicure','Polish Change','/static/photos/mani6.jpg','$25.00'),(18,'pedicure','Basic Pedicure','/static/photos/padi1.jpg','$35.00'),(19,'pedicure','Deluxe Pedicure','/static/photos/padi2.jpg','$50.00'),(20,'pedicure','Polish Change','/static/photos/padi3.jpg','$25.00'),(21,'pedicure','Gel Pedicure','/static/photos/padi4.jpg','$35.00'),(22,'waxing','Eyebrows','/static/photos/wax1.jpg','$10.00'),(23,'waxing','Chin','/static/photos/wax2.jpg','$8.00+'),(24,'waxing','Lip','/static/photos/wax3.jpg','$7.00'),(25,'waxing','Full Face','/static/photos/wax4.jpg','$30.00+'),(26,'waxing','Back','/static/photos/wax5.jpg','$45.00+'),(27,'waxing','Half Arms','/static/photos/wax6.jpg','$25.00+'),(28,'waxing','Full Arms','/static/photos/wax6.jpg','$35.00+'),(29,'waxing','Half Legs','/static/photos/wax7.jpg','$30.00'),(30,'waxing','Full Legs','/static/photos/wax7.jpg','$40.00'),(31,'waxing','Bikini','/static/photos/wax8.jpg','$40+');
/*!40000 ALTER TABLE `services` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sessions`
--

DROP TABLE IF EXISTS `sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sessions` (
  `session_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `session_token` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`session_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `sessions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`CustomerID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sessions`
--

LOCK TABLES `sessions` WRITE;
/*!40000 ALTER TABLE `sessions` DISABLE KEYS */;
/*!40000 ALTER TABLE `sessions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `CustomerID` int NOT NULL AUTO_INCREMENT,
  `UserName` varchar(50) NOT NULL,
  `passcode` varchar(255) NOT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `Phone` varchar(15) NOT NULL,
  `Name` varchar(45) NOT NULL,
  PRIMARY KEY (`CustomerID`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'qwe','qwe','qwe@gmail.com','123123123','Jessi Prowd'),(2,'123','123','123@gmail.com','1231231','Olivia Harper'),(3,'321','scrypt:32768:8:1$A3Y7DkI40RdTtfl4$8506f8a666106facb121cf100ed17485d58bb6086b18fd2baeb4a5ba6a9129e05428e7d675672cdea1de8d0fba3994ca0aab7feab4fb0fe693465c530e738afd','321@gmail.com','321321','Luna Mason'),(4,'111','scrypt:32768:8:1$qyDmLNT1FhQdYiuZ$57339ab8331506006f643dcbebedf7e42ea90bd64bb74ed9fcf6a7afa9248daca36348a17d1674c4ba5cf520fe6c627ff23eaf74444623b1ff7d8a74af3fe5ea','1211@gmail.com','111111','Athena Romano'),(7,'ttt','scrypt:32768:8:1$tn7vM4jVfNTF9gBQ$ac089eb6a87603791aa2941d46597a38a608c03a7e7324ba86c98e0b4fc1648d535514d4f92a68eec4725c5c580af41f73b2dae6f87f2a7aa95f5f8d44c5d73a','ttt@gmail.com','101010','Jack Sparrow'),(8,'101','scrypt:32768:8:1$KxiWL9X9aWjXsxXY$f1c334d4e86aa7edfce8fa9e1b3674e4c9655586a335853fd5cba73d07ab1a0a062fbab6877c424d6516e8dd39fc7e6cb7a1437cea707285763ddfe332b48590','101@gmail.com','101101','Thinh Tran'),(9,'ert','scrypt:32768:8:1$lNYz0XFTVqnbdG2u$d98f43c8e72dedab6fcb6adc6f77dd51273fa94eea003519a7648a560f69120395694e8b370be42396aa8ef0e467d9bc7defbff10636b8d22d5fccdee142d991','thinh2405543926@gmail.com','6092879255','Thinh');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `week_schedule`
--

DROP TABLE IF EXISTS `week_schedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `week_schedule` (
  `id` int NOT NULL AUTO_INCREMENT,
  `managerID` int NOT NULL DEFAULT '101123',
  `time_slot` varchar(10) NOT NULL,
  `monday` varchar(255) DEFAULT '',
  `tuesday` varchar(255) DEFAULT '',
  `wednesday` varchar(255) DEFAULT '',
  `thursday` varchar(255) DEFAULT '',
  `friday` varchar(255) DEFAULT '',
  `saturday` varchar(255) DEFAULT '',
  `sunday` varchar(255) DEFAULT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `time_slot` (`time_slot`),
  KEY `fk_managerID` (`managerID`),
  CONSTRAINT `fk_managerID` FOREIGN KEY (`managerID`) REFERENCES `managers` (`managerID`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `week_schedule`
--

LOCK TABLES `week_schedule` WRITE;
/*!40000 ALTER TABLE `week_schedule` DISABLE KEYS */;
INSERT INTO `week_schedule` VALUES (1,101101,'8:00 AM','Arnab, Fred, Abhi','','Jacob, T','T, Fred, Arnab','Jessi, Fred, Jackson, Tina','trtrt',''),(2,101101,'9:00 AM','','Leo, Jack','','Sony','','Lisa, Jessi, Sony, John',''),(3,101101,'10:00 AM','','','','','','',''),(4,101101,'11:00 AM','','','','','','',''),(5,101101,'12:00 PM','fesdfe','sefs','','esfdf','','',''),(6,101101,'1:00 PM','Fred','','Jacob','Fred','Tina','',''),(7,101123,'2:00 PM','','','','','','',''),(8,101123,'3:00 PM','','','','','','',''),(9,101123,'4:00 PM','Arnab, Thinh','','Thinh','','Jessi','',''),(10,101123,'5:00 PM','','','','','','',''),(11,101123,'6:00 PM','','','','','','',''),(12,101123,'7:00 PM','','Jack, Leo','','','','','');
/*!40000 ALTER TABLE `week_schedule` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-01 14:28:31
