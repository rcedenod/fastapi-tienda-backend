-- MySQL dump 10.13  Distrib 8.0.29, for Win64 (x86_64)
--
-- Host: localhost    Database: cms_db
-- ------------------------------------------------------
-- Server version	8.0.29

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
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category` (
  `CategoryID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(127) NOT NULL,
  `Code` varchar(127) NOT NULL,
  `Summary` text,
  `IsActived` smallint NOT NULL DEFAULT '1',
  `CreatedAt` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`CategoryID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (1,'Libros','LIB','Categoría para libros',1,'2024-04-17 21:16:39'),(2,'Ropa','ROP','Categoría para ropa',1,'2024-04-17 21:16:39'),(3,'Comida','COM','Categoría para alimentos y comestibles',1,'2024-04-17 21:16:39');
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comment`
--

DROP TABLE IF EXISTS `comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comment` (
  `CommentID` int NOT NULL AUTO_INCREMENT,
  `CustomerID` int NOT NULL,
  `Content` text NOT NULL,
  `CreatedAt` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`CommentID`),
  KEY `FK_Customer_idx` (`CustomerID`),
  CONSTRAINT `FK_Customer` FOREIGN KEY (`CustomerID`) REFERENCES `customer` (`CustomerID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment`
--

LOCK TABLES `comment` WRITE;
/*!40000 ALTER TABLE `comment` DISABLE KEYS */;
/*!40000 ALTER TABLE `comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer` (
  `CustomerID` int NOT NULL AUTO_INCREMENT,
  `Fullname` varchar(127) NOT NULL,
  `Email` varchar(127) NOT NULL,
  `Phone` text,
  `CreatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`CustomerID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `email_config`
--

DROP TABLE IF EXISTS `email_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `email_config` (
  `EmailConfigID` int NOT NULL AUTO_INCREMENT,
  `HostAddress` text NOT NULL,
  `HostPort` int NOT NULL,
  `EmailAddress` varchar(255) NOT NULL,
  `EmailUsername` varchar(255) NOT NULL,
  `EmailPassword` text NOT NULL,
  `CreatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`EmailConfigID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `email_config`
--

LOCK TABLES `email_config` WRITE;
/*!40000 ALTER TABLE `email_config` DISABLE KEYS */;
INSERT INTO `email_config` VALUES (1,'smtp-mail.outlook.com',587,'pythoncourse.test10@outlook.com','pythoncourse.test10@outlook.com','gAAAAABmIZ-fy0PU6gCgh1lOfX9vtlO8Y1MRLIFzRZPxK5TyA2XGH5CvnVV1vL69Kx9EWiNHQZvdkQR00BqeD94iQ7d6wxPpTA==','2024-04-18 01:11:45');
/*!40000 ALTER TABLE `email_config` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product` (
  `ProductID` int NOT NULL AUTO_INCREMENT,
  `CategoryID` int NOT NULL,
  `Name` varchar(127) NOT NULL,
  `Code` varchar(127) NOT NULL,
  `Summary` text,
  `Description` text,
  `Price` decimal(10,2) DEFAULT NULL,
  `IsActived` smallint NOT NULL DEFAULT '1',
  `IsDeleted` smallint NOT NULL DEFAULT '0',
  `CreatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ProductID`),
  KEY `FK_CategoryID_idx` (`CategoryID`),
  CONSTRAINT `FK_Category` FOREIGN KEY (`CategoryID`) REFERENCES `category` (`CategoryID`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES (1,1,'Grief Is For People v2','LIB001','Resumen del libro 1','Descripción del libro 1',30.00,1,1,'2024-04-17 21:28:35'),(2,1,'Come and Get It','LIB002','Resumen del libro 2','Descripción del libro 2',20.00,1,0,'2024-04-17 21:28:35'),(3,1,'James','LIB003','Resumen del libro 3','Descripción del libro 3',25.00,1,0,'2024-04-17 21:28:35'),(4,1,'Real Americans','LIB004','Resumen del libro 4','Descripción del libro 4',35.00,1,0,'2024-04-17 21:28:35'),(5,1,'Funny Story','LIB005','Resumen del libro 5','Descripción del libro 5',28.00,1,0,'2024-04-17 21:28:35'),(6,2,'Camiseta','ROP001','Resumen de la camiseta 1','Descripción de la camiseta 1',20.00,1,0,'2024-04-17 21:28:35'),(7,2,'Pantalón','ROP002','Resumen del pantalón 1','Descripción del pantalón 1',40.00,1,0,'2024-04-17 21:28:35'),(8,2,'Vestido','ROP003','Resumen del vestido 1','Descripción del vestido 1',50.00,1,0,'2024-04-17 21:28:35'),(9,2,'Camisa','ROP004','Resumen de la camisa 1','Descripción de la camisa 1',30.00,1,0,'2024-04-17 21:28:35'),(10,2,'Zapatos','ROP005','Resumen de los zapatos 1','Descripción de los zapatos 1',60.00,1,0,'2024-04-17 21:28:35'),(11,3,'Manzana','COM001','Resumen de la manzana 1','Descripción de la manzana 1',1.00,1,0,'2024-04-17 21:28:35'),(12,3,'Pan','COM002','Resumen del pan 1','Descripción del pan 1',2.00,1,0,'2024-04-17 21:28:35'),(13,3,'Lechuga','COM003','Resumen de la lechuga 1','Descripción de la lechuga 1',2.00,1,0,'2024-04-17 21:28:35'),(14,3,'Arroz','COM004','Resumen del arroz 1','Descripción del arroz 1',4.00,1,0,'2024-04-17 21:28:35');
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recovery_code`
--

DROP TABLE IF EXISTS `recovery_code`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recovery_code` (
  `RecoveryCodeID` int NOT NULL AUTO_INCREMENT,
  `UserID` int NOT NULL,
  `Code` varchar(255) NOT NULL,
  `IsActived` smallint NOT NULL DEFAULT '1',
  `CreatedAt` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`RecoveryCodeID`),
  KEY `FK_User_idx` (`UserID`),
  CONSTRAINT `FK_User` FOREIGN KEY (`UserID`) REFERENCES `user` (`UserID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recovery_code`
--

LOCK TABLES `recovery_code` WRITE;
/*!40000 ALTER TABLE `recovery_code` DISABLE KEYS */;
/*!40000 ALTER TABLE `recovery_code` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `UserID` int NOT NULL AUTO_INCREMENT,
  `Fullname` varchar(127) NOT NULL,
  `Email` varchar(255) NOT NULL,
  `Password` varchar(255) NOT NULL,
  `Role` smallint NOT NULL,
  `CreatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`UserID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'Ronald Abu Saleh','ronald.abusaleh@gmail.com','$2b$12$sG675XLkvs1Utnl2mms1Q.vhhM2P.BsgAsy1Dtw2AJHp/S4sKh8wK',1,'2024-04-17 04:41:40');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-18 20:20:37
