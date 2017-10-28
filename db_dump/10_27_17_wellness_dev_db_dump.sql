-- MySQL dump 10.13  Distrib 5.7.8-rc, for Linux (x86_64)
--
-- Host: localhost    Database: wellness_dev_db
-- ------------------------------------------------------
-- Server version	5.7.8-rc

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
-- Table structure for table `credentials`
--

USE wellness_dev_db
DROP TABLE IF EXISTS `credentials`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `credentials` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `password` varchar(128) NOT NULL,
  `f_name` varchar(64) NOT NULL,
  `l_name` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `credentials`
--

LOCK TABLES `credentials` WRITE;
/*!40000 ALTER TABLE `credentials` DISABLE KEYS */;
INSERT INTO `credentials` VALUES (14,'onefineemail@gmail.com','$5$rounds=535000$FH.TeeMApBTsvNwp$Xv3Egs31GLZkcXjoUDGfW4HgDQZz.PHhjPr1AxKSov4','thisGuy','McGillicutty'),(15,'sgkur04@gmail.com','$5$rounds=535000$CDJtj6s6dQq7MWI4$Y4wwPrzHLzPY8SrLytkeKsWnWfXcc8C2ynTgByxhAJ.','Stuart','Kuredjian'),(16,'myemail@gmail.com','$5$rounds=535000$n1Syu2yvV1eI2Ptk$YlUjb/E2kiXOtK9GI4tNVO2f5HXxtdIS86WRDs4YDU0','Buddy','Holly'),(17,'thisemail@gmail.com','$5$rounds=535000$GqFANkUwexbAy1DO$E2pNLUEf3g7HVDcIRD.FLdwQnCHIaioQJvcXIPtJrt8','newguy','newguyenson'),(18,'someone@someplace.com','$5$rounds=535000$j6lqtWArdnnus0.6$DbFhKhqlh93ASzQlu6HIkCyQDzoRxBnErXhj6AOjhL5','Newdude','LN');
/*!40000 ALTER TABLE `credentials` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `experiences`
--

DROP TABLE IF EXISTS `experiences`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `experiences` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `exp_name` varchar(20) NOT NULL,
  `scale` float NOT NULL,
  `date` datetime NOT NULL,
  `count` int(11) NOT NULL DEFAULT '1',
  `type` varchar(10) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_user` (`user_id`),
  CONSTRAINT `experiences_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `credentials` (`id`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `experiences`
--

LOCK TABLES `experiences` WRITE;
/*!40000 ALTER TABLE `experiences` DISABLE KEYS */;
INSERT INTO `experiences` VALUES (33,'kangaroo',4.5,'2017-10-24 00:00:00',2,'positive',14),(34,'element',9,'2017-10-24 00:00:00',1,'positive',14),(35,'monkey',2,'2017-10-24 00:00:00',1,'positive',14),(36,'giraffe',7,'2017-10-24 00:00:00',1,'negative',14),(37,'igloo',3.33333,'2017-10-25 00:00:00',3,'positive',16),(38,'cheese',1,'2017-10-25 00:00:00',1,'negative',16),(39,'balloon',6,'2017-10-25 00:00:00',1,'negative',16),(40,'giraffe',2,'2017-10-25 00:00:00',1,'positive',16),(41,'monkey`',2,'2017-10-27 00:00:00',1,'positive',16),(42,'monkey',2,'2017-10-27 00:00:00',2,'negative',16),(43,'ant',1,'2017-10-27 00:00:00',1,'positive',16),(44,'test',1,'2017-10-27 00:00:00',2,'positive',18),(45,'test',1,'2017-10-27 00:00:00',0,'negative',18),(46,'igloo',4,'2017-10-27 00:00:00',1,'positive',18),(47,'monkey',5,'2017-10-28 00:00:00',1,'positive',16),(48,'pain in butt',5,'2017-10-28 00:00:00',1,'negative',16);
/*!40000 ALTER TABLE `experiences` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-10-28  6:44:37
