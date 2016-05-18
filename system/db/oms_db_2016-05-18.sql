# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 127.0.0.1 (MySQL 5.5.5-10.0.20-MariaDB)
# Database: oms_db
# Generation Time: 2016-05-18 13:48:42 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table orderItems
# ------------------------------------------------------------

DROP TABLE IF EXISTS `orderItems`;

CREATE TABLE `orderItems` (
  `id` int(32) NOT NULL AUTO_INCREMENT,
  `orderId` varchar(32) NOT NULL,
  `refCode` varchar(32) DEFAULT NULL,
  `title` varchar(25) DEFAULT '',
  `aipURI` varchar(32) NOT NULL DEFAULT '',
  `aipTitle` varchar(70) NOT NULL DEFAULT '',
  `levelOfDescription` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `orderId` (`orderId`),
  CONSTRAINT `orderitems_ibfk_1` FOREIGN KEY (`orderId`) REFERENCES `orders` (`order`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table orders
# ------------------------------------------------------------

DROP TABLE IF EXISTS `orders`;

CREATE TABLE `orders` (
  `order` varchar(32) NOT NULL DEFAULT '',
  `title` int(11) DEFAULT NULL,
  `origin` varchar(10) NOT NULL DEFAULT '',
  `endUserOrderNotes` text,
  `archivistOrderNotes` text,
  `orderDate` datetime NOT NULL,
  `validationDate` datetime DEFAULT NULL,
  `plannedDate` datetime DEFAULT NULL,
  `AccessDate` datetime DEFAULT NULL,
  `AccessDateComments` text,
  `userid` varchar(40) NOT NULL DEFAULT '',
  `responsiblePerson` varchar(40) DEFAULT NULL,
  `orderStatus` varchar(10) NOT NULL DEFAULT '',
  `accessRestrictionCode` int(11) DEFAULT NULL,
  `accessRestrictionTextExplanation` varchar(96) DEFAULT '',
  `noteText` text,
  `noteTimestamp` datetime DEFAULT NULL,
  `accessEndDate` datetime DEFAULT NULL,
  `deliveryFormat` varchar(30) DEFAULT '',
  PRIMARY KEY (`order`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;

INSERT INTO `orders` (`order`, `title`, `origin`, `endUserOrderNotes`, `archivistOrderNotes`, `orderDate`, `validationDate`, `plannedDate`, `AccessDate`, `AccessDateComments`, `userid`, `responsiblePerson`, `orderStatus`, `accessRestrictionCode`, `accessRestrictionTextExplanation`, `noteText`, `noteTimestamp`, `accessEndDate`, `deliveryFormat`)
VALUES
	('1',NULL,'',NULL,NULL,'2016-05-18 15:25:13',NULL,NULL,NULL,NULL,'',NULL,'',NULL,NULL,NULL,NULL,NULL,NULL);

/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
