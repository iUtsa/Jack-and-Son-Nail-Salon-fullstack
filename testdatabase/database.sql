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
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appointments`
--

LOCK TABLES `appointments` WRITE;
/*!40000 ALTER TABLE `appointments` DISABLE KEYS */;
INSERT INTO `appointments` VALUES (11,'BK19285',3,19,'2024-11-09','21:52:00','22:22:00'),(12,'BK512354',3,16,'2024-11-07','08:00:00','08:30:00');
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
INSERT INTO `business_hours` VALUES (8,'Monday','09:00:00','19:00:00'),(9,'Tuesday','09:00:00','19:00:00'),(10,'Wednesday','09:00:00','19:00:00'),(11,'Thursday','09:00:00','19:00:00'),(12,'Friday','09:00:00','19:00:00'),(13,'Saturday','09:00:00','19:00:00'),(14,'Sunday','00:00:00','00:00:00');
/*!40000 ALTER TABLE `business_hours` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee`
--

DROP TABLE IF EXISTS `employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee` (
  `EmployeeID` int NOT NULL,
  `Employee_name` varchar(50) NOT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `Phone` varchar(15) NOT NULL,
  `servie_provided` varchar(100) NOT NULL,
  PRIMARY KEY (`EmployeeID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee`
--

LOCK TABLES `employee` WRITE;
/*!40000 ALTER TABLE `employee` DISABLE KEYS */;
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
  `price` varchar(10) NOT NULL,
  PRIMARY KEY (`service_id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `services`
--

LOCK TABLES `services` WRITE;
/*!40000 ALTER TABLE `services` DISABLE KEYS */;
INSERT INTO `services` VALUES (1,'nail-care','Pink & White Full Set','/static/photos/nc1final.jpg','$60.00'),(2,'nail-care','Pink & White Fill In','/static/photos/nc2.jpg','$50.00'),(3,'nail-care','Acrylic Full Set','/static/photos/nc3.jpg','$50.00'),(4,'nail-care','Acrylic Fill In','/static/photos/nc4.jpg','$40.00'),(5,'nail-care','Gel Color Full Set','/static/photos/nc5.jpg','$50.00'),(6,'nail-care','Gel Color Fill In','/static/photos/nc6.jpg','$40.00'),(7,'nail-care','Dipping Powder','/static/photos/nc7.jpg','$50.00'),(8,'nail-care','UV Gel Full Set','/static/photos/nc8.jpg','$60.00'),(9,'nail-care','UV Gel Fill In','/static/photos/nc9.jpg','$45.00'),(10,'nail-care','Nail Repair','/static/photos/nc10.jpg','$5.00'),(11,'nail-care','Cut Down Designs','/static/photos/nc11.jpg','$5.00'),(12,'manicure','Pedicure & Manicure','/static/photos/mani1.jpg','$50.00'),(13,'manicure','Regular Pedicure','/static/photos/mani2.jpg','$30.00'),(14,'manicure','Regular Manicure','/static/photos/mani3.jpg','$20.00'),(15,'manicure','Gel Manicure','/static/photos/mani4.jpg','$35.00'),(16,'manicure','Deluxe Manicure','/static/photos/mani5.jpg','$30.00'),(17,'manicure','Polish Change','/static/photos/mani6.jpg','$25.00'),(18,'pedicure','Basic Pedicure','/static/photos/padi1.jpg','$35.00'),(19,'pedicure','Deluxe Pedicure','/static/photos/padi2.jpg','$50.00'),(20,'pedicure','Polish Change','/static/photos/padi3.jpg','$25.00'),(21,'pedicure','Gel Pedicure','/static/photos/padi4.jpg','$35.00'),(22,'waxing','Eyebrows','/static/photos/wax1.jpg','$10.00'),(23,'waxing','Chin','/static/photos/wax2.jpg','$8.00'),(24,'waxing','Lip','/static/photos/wax3.jpg','$7.00'),(25,'waxing','Full Face','/static/photos/wax4.jpg','$30.00'),(26,'waxing','Back','/static/photos/wax5.jpg','$45.00'),(27,'waxing','Half Arms','/static/photos/wax6.jpg','$25.00'),(28,'waxing','Full Arms','/static/photos/wax6.jpg','$35.00'),(29,'waxing','Half Legs','/static/photos/wax7.jpg','$30.00'),(30,'waxing','Full Legs','/static/photos/wax7.jpg','$40.00'),(31,'waxing','Bikini','/static/photos/wax8.jpg','$40.00');
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
  `User_type` enum('customer','employee') NOT NULL,
  PRIMARY KEY (`CustomerID`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'qwe','qwe','qwe@gmail.com','123123123','customer'),(2,'123','123','123@gmail.com','1231231','customer'),(3,'321','scrypt:32768:8:1$A3Y7DkI40RdTtfl4$8506f8a666106facb121cf100ed17485d58bb6086b18fd2baeb4a5ba6a9129e05428e7d675672cdea1de8d0fba3994ca0aab7feab4fb0fe693465c530e738afd','321@gmail.com','321321','customer'),(4,'111','scrypt:32768:8:1$qyDmLNT1FhQdYiuZ$57339ab8331506006f643dcbebedf7e42ea90bd64bb74ed9fcf6a7afa9248daca36348a17d1674c4ba5cf520fe6c627ff23eaf74444623b1ff7d8a74af3fe5ea','1211@gmail.com','111111','customer'),(7,'ttt','scrypt:32768:8:1$tn7vM4jVfNTF9gBQ$ac089eb6a87603791aa2941d46597a38a608c03a7e7324ba86c98e0b4fc1648d535514d4f92a68eec4725c5c580af41f73b2dae6f87f2a7aa95f5f8d44c5d73a','ttt@gmail.com','101010','customer');
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
  `time_slot` time NOT NULL,
  `monday` varchar(255) DEFAULT NULL,
  `tuesday` varchar(255) DEFAULT NULL,
  `wednesday` varchar(255) DEFAULT NULL,
  `thursday` varchar(255) DEFAULT NULL,
  `friday` varchar(255) DEFAULT NULL,
  `saturday` varchar(255) DEFAULT NULL,
  `sunday` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `time_slot` (`time_slot`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `week_schedule`
--

LOCK TABLES `week_schedule` WRITE;
/*!40000 ALTER TABLE `week_schedule` DISABLE KEYS */;
INSERT INTO `week_schedule` VALUES (1,'09:00:00',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(2,'10:00:00',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(3,'11:00:00',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(4,'12:00:00',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(5,'13:00:00',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(6,'14:00:00',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(7,'15:00:00',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(8,'16:00:00',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(9,'17:00:00',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(10,'18:00:00',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(11,'19:00:00',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
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

-- Dump completed on 2024-11-06 23:16:29
