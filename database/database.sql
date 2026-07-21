CREATE DATABASE  IF NOT EXISTS `medicinereminderdb` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `medicinereminderdb`;
-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: medicinereminderdb
-- ------------------------------------------------------
-- Server version	8.0.46

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
-- Table structure for table `medicinelog`
--

DROP TABLE IF EXISTS `medicinelog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medicinelog` (
  `LogID` int NOT NULL AUTO_INCREMENT,
  `MedicineID` int NOT NULL,
  `TakenDate` date NOT NULL,
  `TakenTime` time NOT NULL,
  PRIMARY KEY (`LogID`),
  KEY `fk_medicine_log_idx` (`MedicineID`),
  CONSTRAINT `fk_medicine_log` FOREIGN KEY (`MedicineID`) REFERENCES `medicines` (`MedicineID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medicinelog`
--

LOCK TABLES `medicinelog` WRITE;
/*!40000 ALTER TABLE `medicinelog` DISABLE KEYS */;
INSERT INTO `medicinelog` VALUES (1,1,'2026-07-16','08:00:00'),(2,1,'2026-07-17','08:02:00'),(3,2,'2026-07-16','21:03:00');
/*!40000 ALTER TABLE `medicinelog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medicines`
--

DROP TABLE IF EXISTS `medicines`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medicines` (
  `MedicineID` int NOT NULL AUTO_INCREMENT,
  `UserID` int NOT NULL,
  `MedicineName` varchar(100) NOT NULL,
  `ExpiryDate` date NOT NULL,
  `Quantity` int NOT NULL,
  `DailyDose` int NOT NULL,
  `ReminderTime` time NOT NULL,
  PRIMARY KEY (`MedicineID`),
  KEY `fk_parent_child_idx` (`UserID`),
  CONSTRAINT `fk_parent_child` FOREIGN KEY (`UserID`) REFERENCES `users` (`UserID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medicines`
--

LOCK TABLES `medicines` WRITE;
/*!40000 ALTER TABLE `medicines` DISABLE KEYS */;
INSERT INTO `medicines` VALUES (1,1,'Dolo 650','2028-05-31',20,2,'08:00:00'),(2,1,'Cetirizine','2027-08-20',16,1,'21:00:00'),(3,2,'Crocin 500','2027-06-16',15,1,'22:00:00');
/*!40000 ALTER TABLE `medicines` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `UserID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(70) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `Password` varchar(225) NOT NULL,
  PRIMARY KEY (`UserID`),
  UNIQUE KEY `Email_UNIQUE` (`Email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Pearl','pearl@gmail.com','pl123'),(2,'Siya','siya22@gmail.com','s456');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-07-21 14:33:09
