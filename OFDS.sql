-- MySQL dump 10.13  Distrib 5.7.24, for osx11.1 (x86_64)
--
-- Host: localhost    Database: OFDS
-- ------------------------------------------------------
-- Server version	8.3.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Customer`
--

DROP TABLE IF EXISTS `Customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Customer` (
  `CustomerID` int NOT NULL AUTO_INCREMENT,
  `CustomerName` varchar(50) DEFAULT NULL,
  `CustomerEmail` varchar(50) DEFAULT NULL,
  `CustomerAddress` varchar(50) DEFAULT NULL,
  `CustomerPaymentType` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`CustomerID`)
) ENGINE=InnoDB AUTO_INCREMENT=1020 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Customer`
--

LOCK TABLES `Customer` WRITE;
/*!40000 ALTER TABLE `Customer` DISABLE KEYS */;
INSERT INTO `Customer` VALUES (1001,'Austin S.','austin123@gmail.com','123 Main St','CashApp'),(1002,'Dartagnan S.','sams456@hotmail.com','456 South Blvd','Credit Card'),(1003,'Vale S.','vale789@gmail.com','789 West Pt','Cash'),(1004,'Lilli G.','lilli012@yahoo.com','012 North Ave','Debit Card'),(1019,'Austin','betaken.ping_0q@icloud.com','123 Test Street','Debit Card');
/*!40000 ALTER TABLE `Customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `DateOrder`
--

DROP TABLE IF EXISTS `DateOrder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DateOrder` (
  `OrdersID` int NOT NULL,
  `TimeOfOrder` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`OrdersID`),
  CONSTRAINT `dateorder_ibfk_1` FOREIGN KEY (`OrdersID`) REFERENCES `Orders` (`OrdersID`),
  CONSTRAINT `dateorder_chk_1` CHECK ((length(`OrdersID`) = 4))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `DateOrder`
--

LOCK TABLES `DateOrder` WRITE;
/*!40000 ALTER TABLE `DateOrder` DISABLE KEYS */;
INSERT INTO `DateOrder` VALUES (4000,'2024-04-19 10:56:15'),(4001,'2024-04-19 10:56:15'),(4002,'2024-04-19 10:56:15'),(4003,'2024-04-19 10:56:15');
/*!40000 ALTER TABLE `DateOrder` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Driver`
--

DROP TABLE IF EXISTS `Driver`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Driver` (
  `DriverID` int NOT NULL,
  `CurrentDriverLocation` varchar(60) DEFAULT NULL,
  `DriverName` varchar(100) DEFAULT NULL,
  `DriverDesc` varchar(300) DEFAULT NULL,
  `OrderIsReceived` tinyint(1) DEFAULT NULL,
  `DriverStarRating` enum('0','1','2','3','4','5') NOT NULL,
  `OrdersID` int NOT NULL,
  `ServiceFee` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`DriverID`),
  KEY `OrdersID` (`OrdersID`),
  CONSTRAINT `driver_ibfk_1` FOREIGN KEY (`OrdersID`) REFERENCES `Orders` (`OrdersID`),
  CONSTRAINT `driver_chk_1` CHECK ((length(`DriverID`) = 4)),
  CONSTRAINT `driver_chk_2` CHECK ((length(`OrdersID`) = 4))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Driver`
--

LOCK TABLES `Driver` WRITE;
/*!40000 ALTER TABLE `Driver` DISABLE KEYS */;
INSERT INTO `Driver` VALUES (7000,'(34.0522° N, 118.2437° W)','Kyle R.','I deliver within a 15 mile radius by car',1,'3',4003,8.99),(7001,'(39.0542° S, 256.2177° E)','Yanin E.','I deliver on the southside within a 5 mile radius by motorbike',1,'3',4002,10.00),(7002,'(40.0542° S, 256.5952° E)','Yanin E.','I deliver on the southside within a 5 mile radius by motorbike',0,'3',4001,10.00),(7003,'(65.4762° N, 159.2470° W)','Ian R.','I deliver within a 7 mile radius by e-bike',1,'4',4000,6.99);
/*!40000 ALTER TABLE `Driver` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `LocationDelivery`
--

DROP TABLE IF EXISTS `LocationDelivery`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `LocationDelivery` (
  `OrdersID` int NOT NULL AUTO_INCREMENT,
  `DeliveryAddress` varchar(300) DEFAULT NULL,
  `PickupAddress` varchar(300) DEFAULT NULL,
  PRIMARY KEY (`OrdersID`),
  CONSTRAINT `locationdelivery_ibfk_1` FOREIGN KEY (`OrdersID`) REFERENCES `Orders` (`OrdersID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `LocationDelivery`
--

LOCK TABLES `LocationDelivery` WRITE;
/*!40000 ALTER TABLE `LocationDelivery` DISABLE KEYS */;
/*!40000 ALTER TABLE `LocationDelivery` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Menu`
--

DROP TABLE IF EXISTS `Menu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Menu` (
  `MenuID` int NOT NULL,
  `RestaurantID` int NOT NULL,
  `MenuItem` varchar(50) DEFAULT NULL,
  `MenuItemDesc` varchar(500) DEFAULT NULL,
  `MenuItemPrice` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`MenuID`),
  KEY `RestaurantID` (`RestaurantID`),
  CONSTRAINT `menu_ibfk_1` FOREIGN KEY (`RestaurantID`) REFERENCES `Restaurant` (`RestaurantID`),
  CONSTRAINT `menu_chk_1` CHECK ((length(`RestaurantID`) = 4))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Menu`
--

LOCK TABLES `Menu` WRITE;
/*!40000 ALTER TABLE `Menu` DISABLE KEYS */;
INSERT INTO `Menu` VALUES (3000,2000,'Burrito Bowl','Burrito bowl with your choice of chicken, barbacoa, or steak',13.99),(3001,2001,'Double-Quarter Pounder with Cheese','Two 1/4 pound angus beef patties, lettuce, tomato, and American cheese. Comes with fries',14.99),(3002,2002,'Brown Sugar Shaken Espresso','Two pumps of our signature brown sugar syrup, blonde roast espresso, a splash of oatmilk, topped with sweet cream cinnamon vanilla cold foam',8.99);
/*!40000 ALTER TABLE `Menu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Orders`
--

DROP TABLE IF EXISTS `Orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Orders` (
  `OrdersID` int NOT NULL,
  `CustomerID` int NOT NULL,
  `RestaurantID` int NOT NULL,
  `OrdersDate` datetime DEFAULT CURRENT_TIMESTAMP,
  `TotalPrice` decimal(10,2) DEFAULT NULL,
  `OrdersStatus` enum('RECEIVED','PENDING','DELIVERED','IN-TRANSIT','CANCELED') NOT NULL,
  `CustomerComment` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`OrdersID`),
  KEY `RestaurantID` (`RestaurantID`),
  KEY `orders_fk_1` (`CustomerID`),
  CONSTRAINT `orders_fk_1` FOREIGN KEY (`CustomerID`) REFERENCES `Customer` (`CustomerID`),
  CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`RestaurantID`) REFERENCES `Restaurant` (`RestaurantID`),
  CONSTRAINT `orders_chk_1` CHECK ((length(`OrdersID`) = 4)),
  CONSTRAINT `orders_chk_2` CHECK ((length(`CustomerID`) = 4)),
  CONSTRAINT `orders_chk_3` CHECK ((length(`RestaurantID`) = 4))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Orders`
--

LOCK TABLES `Orders` WRITE;
/*!40000 ALTER TABLE `Orders` DISABLE KEYS */;
INSERT INTO `Orders` VALUES (4000,1001,2000,'2024-04-19 10:56:15',13.99,'PENDING','Extra chicken, please'),(4001,1002,2001,'2024-04-19 10:56:15',14.99,'DELIVERED','No pickles or mustard, please. Fries extra crispy'),(4002,1003,2002,'2024-04-19 10:56:15',8.99,'IN-TRANSIT','Light ice, no cold foam, please'),(4003,1004,2000,'2024-04-19 10:56:15',13.99,'CANCELED','You guys always forget to add enough cheese');
/*!40000 ALTER TABLE `Orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PaymentInformation`
--

DROP TABLE IF EXISTS `PaymentInformation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `PaymentInformation` (
  `CustomerID` int NOT NULL AUTO_INCREMENT,
  `CardNum` varchar(19) DEFAULT NULL,
  `CardName` varchar(30) DEFAULT NULL,
  `CardExpireDate` varchar(5) DEFAULT NULL,
  `CardCCN` int DEFAULT NULL,
  PRIMARY KEY (`CustomerID`),
  CONSTRAINT `paymentinformation_fk_1` FOREIGN KEY (`CustomerID`) REFERENCES `Customer` (`CustomerID`),
  CONSTRAINT `paymentinformation_chk_1` CHECK ((length(`CardNum`) = 19)),
  CONSTRAINT `paymentinformation_chk_2` CHECK ((length(`CardCCN`) = 3))
) ENGINE=InnoDB AUTO_INCREMENT=1005 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PaymentInformation`
--

LOCK TABLES `PaymentInformation` WRITE;
/*!40000 ALTER TABLE `PaymentInformation` DISABLE KEYS */;
INSERT INTO `PaymentInformation` VALUES (1001,'1234 5678 9101 1123','Austin S.','05/28',123),(1002,'9999 8888 7777 3333','Dartagnan S.','11/30',142),(1003,'1561 4489 6516 6511','Vale S.','06/27',415),(1004,'2656 1656 4982 1615','Lilli G.','07/26',845);
/*!40000 ALTER TABLE `PaymentInformation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Price`
--

DROP TABLE IF EXISTS `Price`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Price` (
  `OrdersID` int NOT NULL,
  `TotalCart` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`OrdersID`),
  CONSTRAINT `price_ibfk_1` FOREIGN KEY (`OrdersID`) REFERENCES `Orders` (`OrdersID`),
  CONSTRAINT `price_chk_1` CHECK ((length(`OrdersID`) = 4))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Price`
--

LOCK TABLES `Price` WRITE;
/*!40000 ALTER TABLE `Price` DISABLE KEYS */;
INSERT INTO `Price` VALUES (4000,20.00),(4001,65.99),(4002,8.99),(4003,13.99);
/*!40000 ALTER TABLE `Price` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Quantity`
--

DROP TABLE IF EXISTS `Quantity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Quantity` (
  `OrdersID` int NOT NULL,
  `Item` varchar(200) DEFAULT NULL,
  `Quantity` int DEFAULT NULL,
  PRIMARY KEY (`OrdersID`),
  CONSTRAINT `quantity_ibfk_1` FOREIGN KEY (`OrdersID`) REFERENCES `Orders` (`OrdersID`),
  CONSTRAINT `quantity_chk_1` CHECK ((length(`OrdersID`) = 4))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Quantity`
--

LOCK TABLES `Quantity` WRITE;
/*!40000 ALTER TABLE `Quantity` DISABLE KEYS */;
INSERT INTO `Quantity` VALUES (4000,'Burrito Bowl',1),(4001,'Burger Combo',2),(4002,'Coffee',1),(4003,'Burrito Bowl',1);
/*!40000 ALTER TABLE `Quantity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Restaurant`
--

DROP TABLE IF EXISTS `Restaurant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Restaurant` (
  `RestaurantID` int NOT NULL,
  `RestaurantName` varchar(50) DEFAULT NULL,
  `RestaurantDesc` varchar(800) DEFAULT NULL,
  `RestaurantStarRating` enum('0','1','2','3','4','5','6') NOT NULL,
  `RestaurantLocation` varchar(50) DEFAULT NULL,
  `Approved` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`RestaurantID`),
  CONSTRAINT `restaurant_chk_1` CHECK ((length(`RestaurantID`) = 4))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Restaurant`
--

LOCK TABLES `Restaurant` WRITE;
/*!40000 ALTER TABLE `Restaurant` DISABLE KEYS */;
INSERT INTO `Restaurant` VALUES (2000,'The Binary Burrito','An award-winning, casual dining spot serving Mexican food with an American Southern influence','3','859 Brefield Way',0),(2001,'Cartesian Grill','A fast-casual burger joint offering over 10k order combinations','4','114 Cheshire Pt',0),(2002,'The Java Hut','A cafe that sources artisan-selected beans to brew specialty coffee and espresso-based drinks','4','114 Tortuga Blvd',1);
/*!40000 ALTER TABLE `Restaurant` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-19 23:26:10
