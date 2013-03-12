-- MySQL dump 10.13  Distrib 5.5.28, for osx10.8 (i386)
--
-- Host: localhost    Database: municonv
-- ------------------------------------------------------
-- Server version	5.5.28

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
-- Table structure for table `alias`
--

DROP TABLE IF EXISTS `alias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alias` (
  `alias_id` int(11) NOT NULL AUTO_INCREMENT,
  `pv_id` int(11) NOT NULL DEFAULT '0',
  `alias` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`alias_id`),
  KEY `Ref_185` (`pv_id`),
  CONSTRAINT `Ref_185` FOREIGN KEY (`pv_id`) REFERENCES `pv` (`pv_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alias`
--

LOCK TABLES `alias` WRITE;
/*!40000 ALTER TABLE `alias` DISABLE KEYS */;
/*!40000 ALTER TABLE `alias` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `beam_parameter`
--

DROP TABLE IF EXISTS `beam_parameter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `beam_parameter` (
  `twiss_id` int(11) NOT NULL AUTO_INCREMENT,
  `element_id` int(11) DEFAULT NULL,
  `model_id` int(11) DEFAULT NULL,
  `pos` double DEFAULT NULL,
  `alpha_x` double DEFAULT NULL,
  `beta_x` double DEFAULT NULL,
  `nu_x` double DEFAULT NULL,
  `eta_x` double DEFAULT NULL,
  `etap_x` double DEFAULT NULL,
  `alpha_y` double DEFAULT NULL,
  `beta_y` double DEFAULT NULL,
  `nu_y` double DEFAULT NULL,
  `eta_y` double DEFAULT NULL,
  `etap_y` double DEFAULT NULL,
  `transfer_matrix` varchar(2047) DEFAULT NULL,
  `co_x` double DEFAULT NULL,
  `co_y` double DEFAULT NULL,
  `index_slice_chk` int(11) DEFAULT NULL,
  `s` double DEFAULT NULL,
  `energy` double DEFAULT NULL,
  `particel_species` varchar(45) DEFAULT NULL,
  `particle mass` double DEFAULT NULL,
  `particle charge` int(11) DEFAULT NULL,
  `beam_charge_density` double DEFAULT NULL,
  `beam_current` double DEFAULT NULL,
  `x` double DEFAULT NULL,
  `xp` double DEFAULT NULL,
  `y` double DEFAULT NULL,
  `yp` double DEFAULT NULL,
  `z` double DEFAULT NULL,
  `zp` double DEFAULT NULL,
  `emit_x` double DEFAULT NULL,
  `emit_y` double DEFAULT NULL,
  `emit_z` double DEFAULT NULL,
  PRIMARY KEY (`twiss_id`),
  KEY `FK_element` (`element_id`),
  KEY `Ref_212` (`model_id`),
  CONSTRAINT `FK_element` FOREIGN KEY (`element_id`) REFERENCES `element` (`element_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Ref_212` FOREIGN KEY (`model_id`) REFERENCES `model` (`model_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `beam_parameter`
--

LOCK TABLES `beam_parameter` WRITE;
/*!40000 ALTER TABLE `beam_parameter` DISABLE KEYS */;
/*!40000 ALTER TABLE `beam_parameter` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `beamline_sequence`
--

DROP TABLE IF EXISTS `beamline_sequence`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `beamline_sequence` (
  `beamline_sequence_id` int(11) NOT NULL AUTO_INCREMENT,
  `sequence_name` varchar(45) DEFAULT NULL,
  `first_element_name` varchar(45) DEFAULT NULL,
  `last_element_name` varchar(45) DEFAULT NULL,
  `previous_section` varchar(45) DEFAULT NULL,
  `sequence_length` double DEFAULT NULL,
  `sequence_description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`beamline_sequence_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `beamline_sequence`
--

LOCK TABLES `beamline_sequence` WRITE;
/*!40000 ALTER TABLE `beamline_sequence` DISABLE KEYS */;
/*!40000 ALTER TABLE `beamline_sequence` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `blsequence__lattice`
--

DROP TABLE IF EXISTS `blsequence__lattice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `blsequence__lattice` (
  `blsequence__lattice_id` int(11) NOT NULL AUTO_INCREMENT,
  `beamline_sequence_id` int(11) DEFAULT NULL,
  `lattice_id` int(11) DEFAULT NULL,
  `beamline_order` int(11) DEFAULT NULL,
  PRIMARY KEY (`blsequence__lattice_id`),
  KEY `Ref_18` (`beamline_sequence_id`),
  KEY `Ref_16` (`lattice_id`),
  CONSTRAINT `Ref_18` FOREIGN KEY (`beamline_sequence_id`) REFERENCES `beamline_sequence` (`beamline_sequence_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Ref_16` FOREIGN KEY (`lattice_id`) REFERENCES `lattice` (`lattice_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `blsequence__lattice`
--

LOCK TABLES `blsequence__lattice` WRITE;
/*!40000 ALTER TABLE `blsequence__lattice` DISABLE KEYS */;
/*!40000 ALTER TABLE `blsequence__lattice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bundle_pull`
--

DROP TABLE IF EXISTS `bundle_pull`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bundle_pull` (
  `bundle_pull_id` int(11) NOT NULL AUTO_INCREMENT,
  `bundle_label` varchar(255) DEFAULT NULL,
  `bundle_identifier` varchar(50) DEFAULT NULL,
  `cable_count` int(11) DEFAULT '1',
  `owner` varchar(50) DEFAULT 'unknown',
  `install_check` int(11) DEFAULT NULL,
  PRIMARY KEY (`bundle_pull_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bundle_pull`
--

LOCK TABLES `bundle_pull` WRITE;
/*!40000 ALTER TABLE `bundle_pull` DISABLE KEYS */;
/*!40000 ALTER TABLE `bundle_pull` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bundlepull__install`
--

DROP TABLE IF EXISTS `bundlepull__install`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bundlepull__install` (
  `bundlepull__install_id` int(11) NOT NULL AUTO_INCREMENT,
  `bundle_pull_id` int(11) NOT NULL,
  `install_id` int(11) NOT NULL DEFAULT '0',
  `path_order` int(11) DEFAULT NULL,
  `validated` int(11) DEFAULT NULL,
  PRIMARY KEY (`bundlepull__install_id`),
  KEY `idx_cable_pull_id` (`bundle_pull_id`),
  KEY `Ref_76` (`install_id`),
  CONSTRAINT `Ref_57` FOREIGN KEY (`bundle_pull_id`) REFERENCES `bundle_pull` (`bundle_pull_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Ref_76` FOREIGN KEY (`install_id`) REFERENCES `install` (`install_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bundlepull__install`
--

LOCK TABLES `bundlepull__install` WRITE;
/*!40000 ALTER TABLE `bundlepull__install` DISABLE KEYS */;
/*!40000 ALTER TABLE `bundlepull__install` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cable`
--

DROP TABLE IF EXISTS `cable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cable` (
  `cable_id` int(11) NOT NULL AUTO_INCREMENT,
  `port_a_id` int(11) DEFAULT NULL,
  `port_b_id` int(11) DEFAULT NULL,
  `bundle_pull_id` int(11) DEFAULT NULL,
  `cable_type_id` int(11) NOT NULL DEFAULT '0',
  `color` varchar(60) DEFAULT NULL,
  `cable_identifier` varchar(50) DEFAULT NULL,
  `port_a_label` varchar(50) DEFAULT NULL,
  `port_b_label` varchar(50) DEFAULT NULL,
  `length_m` float DEFAULT NULL,
  `continuity_check` int(11) DEFAULT NULL,
  `panel_to_device_check` int(11) DEFAULT NULL,
  PRIMARY KEY (`cable_id`),
  KEY `idx_port_a_id` (`port_a_id`),
  KEY `idx_port_b_id` (`port_b_id`),
  KEY `idx_cable_pull_id` (`bundle_pull_id`),
  KEY `idx_cable_type_id` (`cable_type_id`),
  CONSTRAINT `Ref_74` FOREIGN KEY (`port_a_id`) REFERENCES `port` (`port_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Ref_75` FOREIGN KEY (`port_b_id`) REFERENCES `port` (`port_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Ref_68` FOREIGN KEY (`bundle_pull_id`) REFERENCES `bundle_pull` (`bundle_pull_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Ref_121` FOREIGN KEY (`cable_type_id`) REFERENCES `cable_type` (`cable_type_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cable`
--

LOCK TABLES `cable` WRITE;
/*!40000 ALTER TABLE `cable` DISABLE KEYS */;
/*!40000 ALTER TABLE `cable` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cable_type`
--

DROP TABLE IF EXISTS `cable_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cable_type` (
  `cable_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `cable_type` varchar(50) DEFAULT NULL,
  `cable_type_description` varchar(255) DEFAULT NULL,
  `cable_diameter` float DEFAULT NULL,
  `ampacity` double DEFAULT NULL,
  PRIMARY KEY (`cable_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cable_type`
--

LOCK TABLES `cable_type` WRITE;
/*!40000 ALTER TABLE `cable_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `cable_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cabletype__partitiontype`
--

DROP TABLE IF EXISTS `cabletype__partitiontype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cabletype__partitiontype` (
  `cabletype__partitiontype` int(11) NOT NULL AUTO_INCREMENT,
  `cable_type_id` int(11) DEFAULT NULL,
  `partition_type_id` int(11) NOT NULL DEFAULT '0',
  `partition_preference` int(11) DEFAULT NULL,
  PRIMARY KEY (`cabletype__partitiontype`),
  KEY `idx_tray_partition_type_id` (`partition_type_id`),
  KEY `Ref_134` (`cable_type_id`),
  CONSTRAINT `Ref_133` FOREIGN KEY (`partition_type_id`) REFERENCES `partition_type` (`partition_type_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Ref_134` FOREIGN KEY (`cable_type_id`) REFERENCES `cable_type` (`cable_type_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cabletype__partitiontype`
--

LOCK TABLES `cabletype__partitiontype` WRITE;
/*!40000 ALTER TABLE `cabletype__partitiontype` DISABLE KEYS */;
/*!40000 ALTER TABLE `cabletype__partitiontype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cmpnt_type`
--

DROP TABLE IF EXISTS `cmpnt_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cmpnt_type` (
  `cmpnt_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `cmpnt_type_name` varchar(100) NOT NULL,
  `description` text,
  `BNL_part_number` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`cmpnt_type_id`),
  UNIQUE KEY `idx_cmpnt_type_name_unique` (`cmpnt_type_name`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cmpnt_type`
--

LOCK TABLES `cmpnt_type` WRITE;
/*!40000 ALTER TABLE `cmpnt_type` DISABLE KEYS */;
INSERT INTO `cmpnt_type` VALUES (1,'Dipole','35mm dipole magnet',NULL),(2,'Dipole G','90mm dipole magnet',NULL),(3,'Quad A','66mm, SNGL COIL, SHORT QUAD',NULL),(4,'Quad B','66mm, SNGL COIL, SHORT QUAD',NULL),(5,'Quad C','66mm, DBL COIL, LONG QUAD',NULL),(6,'Quad Cp','66mm, LONG, DBL COIL KINKED QUAD',NULL),(7,'Quad D','66mm, DBL COIL, SHORT QUAD',NULL),(8,'Quad D2','66mm, DBL COIL, SHORT QUAD',NULL),(9,'Quad E','66mm, DBL COIL, WIDE QUAD',NULL),(10,'Quad E2','66mm, DBL COIL, WIDE QUAD',NULL),(11,'Quad F','90mm, DBL COIL, SHORT QUAD',NULL),(12,'Sext A','68mm, SHORT SEXTUPOLE',NULL),(13,'Sext B','68mm, SHORT, WIDE SEXTUPOLE',NULL),(14,'Sext C','76mm, LONG SEXTUPOLE',NULL),(15,'Corr A','156mm CORRECTOR',NULL),(16,'Corr C','100mm CORRECTOR',NULL),(17,'Corr D','100mm SKEWED CORRECTOR',NULL),(18,'Corr Fast','FAST AIR CORE CORRECTOR',NULL),(19,'Corr A horizontal','156mm horizontal corrector magnet sub-device',NULL),(20,'Corr C horizontal','100mm horizontal corrector magnet sub-device',NULL),(21,'Corr D horizontal','100mm horizontal skewed corrector magnet sub-device',NULL),(22,'Corr Fast horizontal','horizontal fast air core corrector magnet sub-device',NULL),(23,'Corr A vertical','156mm vertical corrector magnet sub-device',NULL),(24,'Corr C vertical','100mm vertical corrector magnet sub-device',NULL),(25,'Corr D vertical','100mm vertical skewed corrector magnet sub-device',NULL),(26,'Corr Fast vertical','vertical  fast air core corrector magnet sub-device',NULL),(27,'LN Solenoid','solenoid accelerator for linac',NULL),(28,'LN Quadrupole','quadrupole magnet for linac',NULL),(29,'LBT Dipole','dipole magnet for linac to booster transport line',NULL),(30,'LBT Quadrupole 1340','quadrupole magnet with 134mm aperture.',NULL),(31,'LBT Quadrupole 5200','quadrupole magnet with 52mm aperture',NULL),(32,'BS Dipole BD1','Dipole type BD1 for booster ring',NULL),(33,'BS Dipole BD2','Dipole type BD2 for booster ring',NULL),(34,'BS Dipole BF','Dipole type BF for booster ring',NULL),(35,'BS Quadrupole QF','Quadrupole type QF for booster ring',NULL),(36,'BS Quadrupole QD','Quadrupole type QD for booster ring',NULL),(37,'BS Quadrupole QG','Quadrupole type QG for booster ring',NULL),(38,'BS Sextupole SF','Sextupole type SF for booster ring',NULL),(39,'BS Sextupole SD','Sextupole type SF for booster ring',NULL),(40,'BST Dipole','dipole magnet for linac to booster transport line',NULL),(41,'BST Quadrupole 5200','quadrupole magnet with 52mm aperture',NULL);
/*!40000 ALTER TABLE `cmpnt_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cmpnt_type_prop`
--

DROP TABLE IF EXISTS `cmpnt_type_prop`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cmpnt_type_prop` (
  `cmpnt_type_prop_id` int(11) NOT NULL AUTO_INCREMENT,
  `cmpnt_type_id` int(11) NOT NULL DEFAULT '0',
  `cmpnt_type_prop_type_id` int(11) DEFAULT NULL,
  `cmpnt_type_prop_value` varchar(4096) DEFAULT NULL,
  PRIMARY KEY (`cmpnt_type_prop_id`),
  KEY `Ref_188` (`cmpnt_type_prop_type_id`),
  KEY `Ref_189` (`cmpnt_type_id`),
  CONSTRAINT `Ref_188` FOREIGN KEY (`cmpnt_type_prop_type_id`) REFERENCES `cmpnt_type_prop_type` (`cmpnt_type_prop_type_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Ref_189` FOREIGN KEY (`cmpnt_type_id`) REFERENCES `cmpnt_type` (`cmpnt_type_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=70 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cmpnt_type_prop`
--

LOCK TABLES `cmpnt_type_prop` WRITE;
/*!40000 ALTER TABLE `cmpnt_type_prop` DISABLE KEYS */;
INSERT INTO `cmpnt_type_prop` VALUES (1,1,1,'DPL-3500'),(2,2,1,'DPL-9000'),(3,3,1,'QDP-9801'),(4,4,1,'QDW-9802'),(5,5,1,'QDP-9804'),(6,6,1,'QDP-9807'),(7,7,1,'QDP-9809'),(8,8,1,'QDP-9810'),(9,9,1,'QDW-9812'),(10,10,1,'QDW-9813'),(11,11,1,'QDP-9815'),(12,12,1,'STP-9801'),(13,13,1,'STP-9802'),(14,14,1,'STP-9816'),(15,15,1,'CRR-1560'),(16,16,1,'CRR-1000'),(17,17,1,'CRR-1001'),(18,18,1,'CRR-2000'),(19,19,1,'CRR-1560'),(20,20,1,'CRR-1000'),(21,21,1,'CRR-1001'),(22,22,1,'CRR-2000'),(23,23,1,'CRR-1560'),(24,24,1,'CRR-1000'),(25,25,1,'CRR-1001'),(26,26,1,'CRR-2000'),(27,29,2,'{\"standard\": {\"direction\": [\"na\", \"na\", \"na\", \"na\", \"na\", \"na\", \"na\", \"na\", \"na\", \"na\", \"na\", \"na\", \"na\", \"na\", \"na\", \"na\", \"na\", \"na\", \"na\", \"na\", \"na\", \"na\", \"na\"], \"run_number\": [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0], \"current_unit\": \"A\", \"sig_current\": [0.0002, 0.0001, 0.0, 0.0001, 0.0003, 0.0001, 0.0002, 0.0004, 0.0004, 0.0006, 0.0004, 0.0001, 0.0003, 0.0007, 0.0003, 0.0005, 0.0004, 0.0002, 0.0001, 0.0001, 0.0001, 0.0002, 0.0001], \"sig_field\": [0.0, 0.0, 1e-05, 0.0, 0.0, 1e-05, 0.0, 1e-05, 0.0, 1e-05, 1e-05, 0.0, 1e-05, 1e-05, 1e-05, 1e-05, 0.0, 1e-05, 1e-05, 0.0, 0.0, 0.0, 0.0], \"ref_draw\": \"LBT-MG-DPL-4800\", \"field_unit\": \"T-m\", \"magnetic_len_design\": 0.35, \"device_name\": \"LB-B1\", \"current\": [24.9502, 39.9774, 55.0182, 67.0419, 80.0492, 93.0512, 106.0302, 120.0292, 130.0967, 141.0654, 150.0796, 155.0641, 150.0801, 141.0662, 130.0978, 120.0297, 106.0306, 93.0519, 80.0498, 67.0417, 55.0177, 39.9775, 24.9499], \"field\": [-0.04454, -0.07115, -0.09795, -0.11948, -0.14267, -0.16584, -0.18889, -0.21358, -0.2312, -0.25018, -0.26555, -0.27384, -0.26661, -0.25222, -0.23357, -0.21598, -0.19124, -0.16813, -0.14492, -0.12165, -0.10011, -0.07325, -0.04637], \"magnetic_len\": [\"\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"\"], \"brho_unit\": \"T-m\", \"brho\": 0.6671400000000001, \"energy_default\": 0.2, \"elem_name\": \"LB-B1\", \"serial\": 3, \"i2b\": [0, \"0.00176598175172*input + 0.00176598175172\"]}}'),(28,30,2,'{\"standard\": {\"direction\": [\"na\", \"na\", \"na\", \"na\", \"na\"], \"current_unit\": \"A\", \"sig_current\": [0.00048, 0.00049, 0.00059, 0.00205, 0.00101], \"sig_field\": [4e-06, 6e-06, 1.4e-05, 7e-06, 1.1e-05], \"ref_draw\": \"LBT-MG-QDP-1340\", \"field_unit\": \"T\", \"magnetic_len_design\": 0.25, \"device_name\": \"LB-Q6\", \"current\": [46.89635, 95.02085, 119.92201, 150.00661, 175.09815], \"field\": [0.31967, 0.647159, 0.816403, 1.019623, 1.187596], \"magnetic_len\": [\"\", \"\", \"\", \"\", \"\"], \"b2k\": [0, \"input/(3.335646*energy)\", 2], \"energy_default\": 0.2, \"elem_name\": \"LB-Q6\", \"serial\": 1, \"i2b\": [0, \"0.00678131127601*input + 0.00200218264515\"]}}'),(29,32,2,'{\"complex\": {\"1\": {\"i2b\": [1, \"2.717329e-13*input**4 -4.50853e-10*input**3 + 2.156812e-07*input**2 + 0.001495718*input + 0.0014639\"], \"field_unit\": \"T\", \"current_unit\": \"A\", \"description\": \"Dipole field component for a combined funbction magnet\"}, \"3\": {\"i2b\": [1, \"-7.736754e-11*input**4 + 1.078356e-07*input**3 -4.27955e-05*input**2 + 0.061426*input + 0.031784\"], \"field_unit\": \"T/m^2\", \"current_unit\": \"A\", \"description\": \"Sextupole field component for a combined funbction magnet\"}, \"2\": {\"i2b\": [1, \"1.239146e-12*input**4 -2.242334e-09*input**3 + 1.117486e-06*input**2 + 0.007377142*input + 0.007218819\"], \"field_unit\": \"T/m\", \"current_unit\": \"A\", \"description\": \"Quadrupole field component for a combined funbction magnet\"}}, \"standard\": {\"field_unit\": \"T\", \"current_unit\": \"A\", \"b2i\": [1, \"-33.289411*input**4 + 84.116293*input**3 -61.320653*input**2 + 668.452373*input -0.969042\"]}}'),(30,33,2,'{\"complex\": {\"1\": {\"i2b\": [1, \"2.407631e-13*input**4 -4.006765e-10*input**3 + 1.924432e-07*input**2 + 0.001497716*input + 0.001682902\"], \"field_unit\": \"T\", \"current_unit\": \"A\", \"description\": \"Dipole field component for a combined funbction magnet\"}, \"3\": {\"i2b\": [1, \"-6.877786e-11*input**4 + 9.583012e-08*input**3 -3.743725e-05*input**2 + 0.060833*input + 0.073836\"], \"field_unit\": \"T/m^2\", \"current_unit\": \"A\", \"description\": \"Sextupole field component for a combined funbction magnet\"}, \"2\": {\"i2b\": [1, \"1.37413e-12*input**4 -2.357779e-09*input**3 + 1.134637e-06*input**2 + 0.00736757*input + 0.008791449\"], \"field_unit\": \"T/m\", \"current_unit\": \"A\", \"description\": \"Quadrupole field component for a combined funbction magnet\"}}, \"standard\": {\"field_unit\": \"T\", \"current_unit\": \"A\", \"b2i\": [1, \"-29.580511*input**4 + 74.960874*input**3 -54.87453*input**2 + 667.626806*input -1.115913\"]}}'),(31,34,2,'{\"complex\": {\"1\": {\"i2b\": [1, \"1.133858e-14*input**4 -3.226502e-11*input**3 + 2.837643e-08*input**2 + 0.0005236598*input + 0.0009995262\"], \"field_unit\": \"T\", \"current_unit\": \"A\", \"description\": \"Dipole field component for a combined funbction magnet\"}, \"3\": {\"i2b\": [1, \"4.297231e-11*input**4 -6.886472e-08*input**3 + 3.374462e-05*input**2 + 0.034619*input + 0.30835\"], \"field_unit\": \"T/m^2\", \"current_unit\": \"A\", \"description\": \"Sextupole field component for a combined funbction magnet\"}, \"2\": {\"i2b\": [1, \"4.116128e-13*input**4 -9.158697e-10*input**3 + 6.821702e-07*input**2 + 0.009293128*input + 0.021007\"], \"field_unit\": \"T/m\", \"current_unit\": \"A\", \"description\": \"Quadrupole field component for a combined funbction magnet\"}}, \"standard\": {\"field_unit\": \"T\", \"current_unit\": \"A\", \"b2i\": [1, \"-294.399726*input**4 + 427.035922*input**3 -195.057031*input**2 + 1909.882*input -1.906891\"]}}'),(32,35,2,'{\"standard\": {\"i2b\": [1, \"-4.980045e-09*input**4 + 1.158642e-06*input**3 -7.272479e-05*input**2 + 0.126664*input + 0.038426\"], \"field_unit\": \"T/m\", \"current_unit\": \"A\", \"b2i\": [1, \"0.000221587*input**4 -0.006875003*input**3 + 0.061032*input**2 + 7.809981*input -0.256296\"]}}'),(33,36,2,'{\"standard\": {\"i2b\": [1, \"-4.722752e-09*input**4 + 1.074093e-06*input**3 -6.383258e-05*input**2 + 0.126074*input + 0.04242\"], \"field_unit\": \"T/m\", \"current_unit\": \"A\", \"b2i\": [1, \"0.0002132786*input**4 -0.006507694*input**3 + 0.055993*input**2 + 7.850111*input -0.29104\"]}}'),(34,37,2,'{\"standard\": {\"i2b\": [1, \"-4.896012e-09*input**4 + 1.126162e-06*input**3 -6.877026e-05*input**2 + 0.126352*input + 0.040868\"], \"field_unit\": \"T/m\", \"current_unit\": \"A\", \"b2i\": [1, \"0.0002203189*input**4 -0.006781118*input**3 + 0.059295*input**2 + 7.829313*input -0.276279\"]}}'),(35,38,2,'{\"standard\": {\"i2b\": [1, \"0.003588652*input**4 -0.053174*input**3 + 0.260755*input**2 + 77.374153*input -11.641088\"], \"field_unit\": \"T/m^2\", \"current_unit\": \"A\", \"b2i\": [1, \"-1.254857e-12*input**4 + 1.387766e-09*input**3 -5.019888e-07*input**2 + 0.012911*input + 0.150391\"]}}'),(36,39,2,'{\"standard\": {\"i2b\": [1, \"0.004355193*input**4 -0.075572*input**3 + 0.44161*input**2 + 76.776102*input -10.94581\"], \"field_unit\": \"T/m^2\", \"current_unit\": \"A\", \"b2i\": [1, \"-1.532404e-12*input**4 + 1.996622e-09*input**3 -8.688711e-07*input**2 + 0.013002*input + 0.142524\"]}}'),(37,40,2,'{\"standard\": {\"current_unit\": \"A\", \"ref_draw\": \"BST-MG-DPL-9035\", \"field_unit\": \"T-m\", \"magnetic_len_design\": 1.4, \"device_name\": \"BS-B2\", \"current\": [50.0, 100.0, 150.0, 200.0, 250.0, 300.0, 315.0, 320.0, 325.0, 330.0, 350.0, \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", 0.0, 1.0, 2.0, 3.0, 4.0], \"field\": [1868.0, 3712.0, 5553.0, 7381.2, 9195.4, 10949.9, 11464.7, 11633.4, 11797.6, 11946.3, 12563.0, \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", \"\", 0.0, 28.0, 51.5, 76.433333, 106.466667], \"brho_unit\": \"T-m\", \"brho\": 10.007100000000001, \"energy_default\": 3.0, \"elem_name\": \"BS-B2\", \"serial\": 1, \"i2b\": [0, \"0.00501981411291*input + 0.0205207863268\"]}}'),(38,5,3,'0.448'),(39,4,3,'0.25'),(40,3,3,'0.25'),(41,11,3,'0.283'),(42,9,3,'0.275'),(43,7,3,'0.275'),(44,2,3,'2.62'),(45,1,3,'2.62'),(46,31,3,'0.15'),(47,40,3,'1.4'),(48,13,3,'0.2'),(49,14,3,'0.25'),(50,12,3,'0.2'),(51,28,3,'0.1'),(52,35,3,'0.3'),(53,33,3,'1.3'),(54,32,3,'1.3'),(55,15,3,'0.3'),(56,17,3,'0.2'),(57,30,3,'0.25'),(58,37,3,'0.3'),(59,36,3,'0.3'),(60,6,3,'0.448'),(61,16,3,'0.2'),(62,39,3,'0.12'),(63,41,3,'0.35'),(64,38,3,'0.12'),(65,18,3,'0.044'),(66,29,3,'0.35'),(67,10,3,'0.275'),(68,8,3,'0.275'),(69,34,3,'1.24');
/*!40000 ALTER TABLE `cmpnt_type_prop` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cmpnt_type_prop_type`
--

DROP TABLE IF EXISTS `cmpnt_type_prop_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cmpnt_type_prop_type` (
  `cmpnt_type_prop_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `cmpnt_type_prop_type_name` varchar(255) DEFAULT NULL,
  `cmpnt_type_prop_type_desc` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`cmpnt_type_prop_type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cmpnt_type_prop_type`
--

LOCK TABLES `cmpnt_type_prop_type` WRITE;
/*!40000 ALTER TABLE `cmpnt_type_prop_type` DISABLE KEYS */;
INSERT INTO `cmpnt_type_prop_type` VALUES (1,'Reference Drawing','Reference Drawing'),(2,'municonv','unit conversion parameters for NSLS II magnets'),(3,'design length','design magnetic length');
/*!40000 ALTER TABLE `cmpnt_type_prop_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cmpnt_type_prop_type_enum`
--

DROP TABLE IF EXISTS `cmpnt_type_prop_type_enum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cmpnt_type_prop_type_enum` (
  `cmpnt_type_prop_type_enum_id` int(11) NOT NULL AUTO_INCREMENT,
  `cmpnt_type_prop_type_id` int(11) DEFAULT NULL,
  `cmpnt_type_prop_type_enum` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`cmpnt_type_prop_type_enum_id`),
  KEY `Ref_193` (`cmpnt_type_prop_type_id`),
  CONSTRAINT `Ref_193` FOREIGN KEY (`cmpnt_type_prop_type_id`) REFERENCES `cmpnt_type_prop_type` (`cmpnt_type_prop_type_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cmpnt_type_prop_type_enum`
--

LOCK TABLES `cmpnt_type_prop_type_enum` WRITE;
/*!40000 ALTER TABLE `cmpnt_type_prop_type_enum` DISABLE KEYS */;
/*!40000 ALTER TABLE `cmpnt_type_prop_type_enum` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cmpnttype__cognizant`
--

DROP TABLE IF EXISTS `cmpnttype__cognizant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cmpnttype__cognizant` (
  `cmpnttype__cognizant_id` int(11) NOT NULL AUTO_INCREMENT,
  `cmpnt_type_id` int(11) DEFAULT '0',
  `person_id` int(11) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  `cmpnt_type_status` enum('in progress','complete') DEFAULT NULL,
  `cmpnt_type_status_date` datetime DEFAULT NULL,
  `last_modified_date` datetime DEFAULT NULL,
  PRIMARY KEY (`cmpnttype__cognizant_id`),
  KEY `Ref_190` (`cmpnt_type_id`),
  KEY `Ref_191` (`person_id`),
  KEY `Ref_243` (`role_id`),
  CONSTRAINT `Ref_190` FOREIGN KEY (`cmpnt_type_id`) REFERENCES `cmpnt_type` (`cmpnt_type_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Ref_191` FOREIGN KEY (`person_id`) REFERENCES `person` (`person_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Ref_243` FOREIGN KEY (`role_id`) REFERENCES `role` (`role_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cmpnttype__cognizant`
--

LOCK TABLES `cmpnttype__cognizant` WRITE;
/*!40000 ALTER TABLE `cmpnttype__cognizant` DISABLE KEYS */;
/*!40000 ALTER TABLE `cmpnttype__cognizant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cmpnttype__document`
--

DROP TABLE IF EXISTS `cmpnttype__document`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cmpnttype__document` (
  `cmpnttype__document_id` int(11) NOT NULL AUTO_INCREMENT,
  `document_id` int(11) DEFAULT NULL,
  `cmpnt_type_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`cmpnttype__document_id`),
  KEY `Ref_159` (`cmpnt_type_id`),
  KEY `Ref_148` (`document_id`),
  CONSTRAINT `Ref_159` FOREIGN KEY (`cmpnt_type_id`) REFERENCES `cmpnt_type` (`cmpnt_type_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Ref_148` FOREIGN KEY (`document_id`) REFERENCES `document` (`document_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cmpnttype__document`
--

LOCK TABLES `cmpnttype__document` WRITE;
/*!40000 ALTER TABLE `cmpnttype__document` DISABLE KEYS */;
/*!40000 ALTER TABLE `cmpnttype__document` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cmpnttype__interface`
--

DROP TABLE IF EXISTS `cmpnttype__interface`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cmpnttype__interface` (
  `cmpnttype__interface_id` int(11) NOT NULL AUTO_INCREMENT,
  `cmpnt_type_id` int(11) NOT NULL,
  `interface_id` int(11) NOT NULL,
  `required` tinyint(1) DEFAULT NULL,
  `max_children` int(11) DEFAULT '0',
  PRIMARY KEY (`cmpnttype__interface_id`),
  UNIQUE KEY `idx_cmpnt_type_interface_unique` (`cmpnt_type_id`,`interface_id`,`required`),
  KEY `idx_cmpnt_type_id` (`cmpnt_type_id`),
  KEY `idx_cmpnt_type_if_type_id` (`interface_id`,`cmpnt_type_id`),
  CONSTRAINT `cmpnt_type_if_ibfk_1` FOREIGN KEY (`cmpnt_type_id`) REFERENCES `cmpnt_type` (`cmpnt_type_id`),
  CONSTRAINT `cmpnt_type_if_ibfk_3` FOREIGN KEY (`interface_id`) REFERENCES `interface` (`interface_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cmpnttype__interface`
--

LOCK TABLES `cmpnttype__interface` WRITE;
/*!40000 ALTER TABLE `cmpnttype__interface` DISABLE KEYS */;
/*!40000 ALTER TABLE `cmpnttype__interface` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cmpnttype__porttype`
--

DROP TABLE IF EXISTS `cmpnttype__porttype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cmpnttype__porttype` (
  `cmpnttype__porttype_id` int(11) NOT NULL AUTO_INCREMENT,
  `cmpnt_type_id` int(11) NOT NULL,
  `port_type_id` int(11) NOT NULL,
  `port_name` varchar(40) NOT NULL,
  `port_order` int(11) NOT NULL,
  PRIMARY KEY (`cmpnttype__porttype_id`),
  UNIQUE KEY `idx_cmpnt_type_port_name_unique` (`cmpnt_type_id`,`port_name`),
  UNIQUE KEY `idx_cmpnt_type_order_unique` (`cmpnt_type_id`,`port_order`),
  KEY `idx_cmpnt_type_id_cpt` (`cmpnt_type_id`),
  KEY `idx_port_type_id_cpt` (`port_type_id`),
  CONSTRAINT `cmpnttype__porttype_ibfk_1` FOREIGN KEY (`cmpnt_type_id`) REFERENCES `cmpnt_type` (`cmpnt_type_id`),
  CONSTRAINT `cmpnttype__porttype_ibfk_2` FOREIGN KEY (`port_type_id`) REFERENCES `port_type` (`port_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cmpnttype__porttype`
--

LOCK TABLES `cmpnttype__porttype` WRITE;
/*!40000 ALTER TABLE `cmpnttype__porttype` DISABLE KEYS */;
/*!40000 ALTER TABLE `cmpnttype__porttype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cmpnttype__vendor`
--

DROP TABLE IF EXISTS `cmpnttype__vendor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cmpnttype__vendor` (
  `cmpnttype__vendor_id` int(11) NOT NULL AUTO_INCREMENT,
  `vendor_id` int(11) DEFAULT NULL,
  `cmpnt_type_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`cmpnttype__vendor_id`),
  KEY `Ref_236` (`vendor_id`),
  KEY `Ref_242` (`cmpnt_type_id`),
  CONSTRAINT `Ref_236` FOREIGN KEY (`vendor_id`) REFERENCES `vendor` (`vendor_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Ref_242` FOREIGN KEY (`cmpnt_type_id`) REFERENCES `cmpnt_type` (`cmpnt_type_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cmpnttype__vendor`
--

LOCK TABLES `cmpnttype__vendor` WRITE;
/*!40000 ALTER TABLE `cmpnttype__vendor` DISABLE KEYS */;
INSERT INTO `cmpnttype__vendor` VALUES (1,1,16),(2,1,17),(3,1,15),(4,2,3),(5,2,5),(6,2,6),(7,3,7),(8,2,8),(9,4,11),(10,5,11),(11,2,4),(12,3,9),(13,2,10),(14,6,12),(15,5,13),(16,4,14),(17,5,14),(18,7,27),(19,7,28),(20,8,29),(21,8,30),(22,8,31),(23,2,32),(24,2,33),(25,2,34),(26,2,35),(27,2,36),(28,2,37),(29,2,38),(30,2,39),(31,8,40),(32,8,41);
/*!40000 ALTER TABLE `cmpnttype__vendor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `conductor`
--

DROP TABLE IF EXISTS `conductor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `conductor` (
  `conductor_id` int(11) NOT NULL AUTO_INCREMENT,
  `cable_id` int(11) NOT NULL,
  `pin_a_id` int(11) DEFAULT NULL,
  `pin_b_id` int(11) DEFAULT NULL,
  `signal_desc_id` int(11) DEFAULT NULL,
  `signal_name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`conductor_id`),
  KEY `idx_cable_id` (`cable_id`),
  KEY `idx_pin_a_id` (`pin_a_id`),
  KEY `idx_pin_b_id` (`pin_b_id`),
  KEY `Ref_245` (`signal_desc_id`),
  CONSTRAINT `conductor_ibfk_1` FOREIGN KEY (`cable_id`) REFERENCES `cable` (`cable_id`),
  CONSTRAINT `Ref_245` FOREIGN KEY (`signal_desc_id`) REFERENCES `signal_desc` (`signal_desc_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Ref_246` FOREIGN KEY (`pin_b_id`) REFERENCES `pin` (`pin_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Ref_247` FOREIGN KEY (`pin_a_id`) REFERENCES `pin` (`pin_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `conductor`
--

LOCK TABLES `conductor` WRITE;
/*!40000 ALTER TABLE `conductor` DISABLE KEYS */;
/*!40000 ALTER TABLE `conductor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `document`
--

DROP TABLE IF EXISTS `document`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `document` (
  `document_id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(255) NOT NULL DEFAULT '0',
  `document_title` varchar(255) DEFAULT NULL,
  `document_type` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`document_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `document`
--

LOCK TABLES `document` WRITE;
/*!40000 ALTER TABLE `document` DISABLE KEYS */;
/*!40000 ALTER TABLE `document` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `element`
--

DROP TABLE IF EXISTS `element`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `element` (
  `element_id` int(11) NOT NULL AUTO_INCREMENT,
  `lattice_id` int(11) DEFAULT NULL,
  `element_type_id` int(11) DEFAULT NULL,
  `element_name` varchar(45) DEFAULT NULL,
  `element_order` int(11) DEFAULT NULL,
  `insert_date` datetime DEFAULT NULL,
  `created_by` varchar(45) DEFAULT NULL,
  `s` double DEFAULT NULL,
  `length` double DEFAULT NULL,
  `dx` double DEFAULT NULL,
  `dy` double DEFAULT NULL,
  `dz` double DEFAULT NULL,
  `pitch` double DEFAULT NULL,
  `yaw` double DEFAULT NULL,
  `roll` double DEFAULT NULL,
  PRIMARY KEY (`element_id`),
  KEY `FK_lattice_element` (`lattice_id`),
  KEY `FK_element_type` (`element_type_id`),
  CONSTRAINT `FK_lattice_element` FOREIGN KEY (`lattice_id`) REFERENCES `lattice` (`lattice_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FK_element_type` FOREIGN KEY (`element_type_id`) REFERENCES `element_type` (`element_type_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `element`
--

LOCK TABLES `element` WRITE;
/*!40000 ALTER TABLE `element` DISABLE KEYS */;
/*!40000 ALTER TABLE `element` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `element__install`
--

DROP TABLE IF EXISTS `element__install`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `element__install` (
  `element__install_id` int(11) NOT NULL,
  `element_id` int(11) DEFAULT NULL,
  `install_id` int(11) DEFAULT NULL,
  `slice` int(11) DEFAULT NULL,
  `index` int(11) DEFAULT NULL,
  PRIMARY KEY (`element__install_id`),
  KEY `FK_element_install` (`element_id`),
  KEY `Ref_216` (`install_id`),
  CONSTRAINT `FK_element_install` FOREIGN KEY (`element_id`) REFERENCES `element` (`element_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Ref_216` FOREIGN KEY (`install_id`) REFERENCES `install` (`install_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `element__install`
--

LOCK TABLES `element__install` WRITE;
/*!40000 ALTER TABLE `element__install` DISABLE KEYS */;
/*!40000 ALTER TABLE `element__install` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `element_prop`
--

DROP TABLE IF EXISTS `element_prop`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `element_prop` (
  `element_prop_id` int(11) NOT NULL AUTO_INCREMENT,
  `element_id` int(11) DEFAULT NULL,
  `element_type_prop_id` int(11) DEFAULT NULL,
  `element_prop_string` varchar(255) DEFAULT NULL,
  `element_prop_int` int(11) DEFAULT NULL,
  `element_prop_double` double DEFAULT NULL,
  `element_prop_index` int(11) DEFAULT NULL,
  PRIMARY KEY (`element_prop_id`),
  KEY `Ref_17` (`element_type_prop_id`),
  KEY `FK_element_id` (`element_id`),
  CONSTRAINT `Ref_17` FOREIGN KEY (`element_type_prop_id`) REFERENCES `element_type_prop` (`element_type_prop_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FK_element_id` FOREIGN KEY (`element_id`) REFERENCES `element` (`element_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `element_prop`
--

LOCK TABLES `element_prop` WRITE;
/*!40000 ALTER TABLE `element_prop` DISABLE KEYS */;
/*!40000 ALTER TABLE `element_prop` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `element_type`
--

DROP TABLE IF EXISTS `element_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `element_type` (
  `element_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `element_type` varchar(45) DEFAULT NULL,
  `element_type_description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`element_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `element_type`
--

LOCK TABLES `element_type` WRITE;
/*!40000 ALTER TABLE `element_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `element_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `element_type_prop`
--

DROP TABLE IF EXISTS `element_type_prop`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `element_type_prop` (
  `element_type_prop_id` int(11) NOT NULL AUTO_INCREMENT,
  `element_type_id` int(11) DEFAULT NULL,
  `element_type_prop_name` varchar(45) DEFAULT NULL,
  `element_type_prop_description` varchar(255) DEFAULT NULL,
  `element_type_prop_default` varchar(255) DEFAULT NULL,
  `element_type_prop_unit` varchar(45) DEFAULT NULL,
  `element_type_prop_datatype` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`element_type_prop_id`),
  KEY `Ref_230` (`element_type_id`),
  CONSTRAINT `Ref_230` FOREIGN KEY (`element_type_id`) REFERENCES `element_type` (`element_type_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `element_type_prop`
--

LOCK TABLES `element_type_prop` WRITE;
/*!40000 ALTER TABLE `element_type_prop` DISABLE KEYS */;
/*!40000 ALTER TABLE `element_type_prop` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `elog_attachment`
--

DROP TABLE IF EXISTS `elog_attachment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `elog_attachment` (
  `elog_attachment_id` int(11) NOT NULL AUTO_INCREMENT,
  `elog_entry_id` int(11) NOT NULL DEFAULT '0',
  `mime_type` varchar(50) DEFAULT NULL,
  `data` text,
  `url` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`elog_attachment_id`),
  KEY `Ref_175` (`elog_entry_id`),
  CONSTRAINT `Ref_175` FOREIGN KEY (`elog_entry_id`) REFERENCES `elog_entry` (`elog_entry_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `elog_attachment`
--

LOCK TABLES `elog_attachment` WRITE;
/*!40000 ALTER TABLE `elog_attachment` DISABLE KEYS */;
/*!40000 ALTER TABLE `elog_attachment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `elog_book`
--

DROP TABLE IF EXISTS `elog_book`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `elog_book` (
  `elog_book_id` int(11) NOT NULL,
  `elog_book_name` varchar(50) DEFAULT NULL,
  `elog_book_type` varchar(50) DEFAULT NULL,
  `elog_book_group` varchar(50) DEFAULT NULL,
  `elog_book_start_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`elog_book_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `elog_book`
--

LOCK TABLES `elog_book` WRITE;
/*!40000 ALTER TABLE `elog_book` DISABLE KEYS */;
/*!40000 ALTER TABLE `elog_book` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `elog_entry`
--

DROP TABLE IF EXISTS `elog_entry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `elog_entry` (
  `elog_entry_id` int(11) NOT NULL AUTO_INCREMENT,
  `elog_book_id` int(11) DEFAULT NULL,
  `author` varchar(50) NOT NULL DEFAULT 'anon',
  `elog_entry` text,
  `elog_thread` int(11) NOT NULL DEFAULT '0',
  `elog_entry_create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `author_IP` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`elog_entry_id`),
  KEY `Ref_166` (`elog_book_id`),
  CONSTRAINT `Ref_166` FOREIGN KEY (`elog_book_id`) REFERENCES `elog_book` (`elog_book_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `elog_entry`
--

LOCK TABLES `elog_entry` WRITE;
/*!40000 ALTER TABLE `elog_entry` DISABLE KEYS */;
/*!40000 ALTER TABLE `elog_entry` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `elog_tag`
--

DROP TABLE IF EXISTS `elog_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `elog_tag` (
  `elog_tag_id` int(11) NOT NULL AUTO_INCREMENT,
  `elog_tag` char(50) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`elog_tag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `elog_tag`
--

LOCK TABLES `elog_tag` WRITE;
/*!40000 ALTER TABLE `elog_tag` DISABLE KEYS */;
/*!40000 ALTER TABLE `elog_tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `elogentry__document`
--

DROP TABLE IF EXISTS `elogentry__document`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `elogentry__document` (
  `elogentry__document_id` int(11) NOT NULL AUTO_INCREMENT,
  `elog_entry_id` int(11) NOT NULL DEFAULT '0',
  `document_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`elogentry__document_id`),
  KEY `Ref_237` (`document_id`),
  KEY `Ref_238` (`elog_entry_id`),
  CONSTRAINT `Ref_237` FOREIGN KEY (`document_id`) REFERENCES `document` (`document_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Ref_238` FOREIGN KEY (`elog_entry_id`) REFERENCES `elog_entry` (`elog_entry_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `elogentry__document`
--

LOCK TABLES `elogentry__document` WRITE;
/*!40000 ALTER TABLE `elogentry__document` DISABLE KEYS */;
/*!40000 ALTER TABLE `elogentry__document` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `elogentry__elogtag`
--

DROP TABLE IF EXISTS `elogentry__elogtag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `elogentry__elogtag` (
  `elogentry__elogtag_id` int(11) NOT NULL AUTO_INCREMENT,
  `elog_tag_id` int(11) NOT NULL DEFAULT '0',
  `elog_entry_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`elogentry__elogtag_id`),
  KEY `Ref_128` (`elog_tag_id`),
  KEY `Ref_127` (`elog_entry_id`),
  CONSTRAINT `Ref_128` FOREIGN KEY (`elog_tag_id`) REFERENCES `elog_tag` (`elog_tag_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Ref_127` FOREIGN KEY (`elog_entry_id`) REFERENCES `elog_entry` (`elog_entry_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `elogentry__elogtag`
--

LOCK TABLES `elogentry__elogtag` WRITE;
/*!40000 ALTER TABLE `elogentry__elogtag` DISABLE KEYS */;
/*!40000 ALTER TABLE `elogentry__elogtag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `elogentry__install`
--

DROP TABLE IF EXISTS `elogentry__install`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `elogentry__install` (
  `elogentry__install_id` int(11) NOT NULL AUTO_INCREMENT,
  `install_id` int(11) NOT NULL DEFAULT '0',
  `elog_entry_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`elogentry__install_id`),
  KEY `Ref_130` (`install_id`),
  KEY `Ref_131` (`elog_entry_id`),
  CONSTRAINT `Ref_130` FOREIGN KEY (`install_id`) REFERENCES `install` (`install_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Ref_131` FOREIGN KEY (`elog_entry_id`) REFERENCES `elog_entry` (`elog_entry_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `elogentry__install`
--

LOCK TABLES `elogentry__install` WRITE;
/*!40000 ALTER TABLE `elogentry__install` DISABLE KEYS */;
/*!40000 ALTER TABLE `elogentry__install` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fld`
--

DROP TABLE IF EXISTS `fld`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fld` (
  `fld_id` int(11) NOT NULL AUTO_INCREMENT,
  `rec_id` int(11) DEFAULT NULL,
  `fld_type_id` int(11) DEFAULT NULL,
  `fld_val` varchar(128) DEFAULT NULL,
  `ioc_resource_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`fld_id`),
  KEY `idx_fld_val` (`fld_val`),
  KEY `idx_rec_id` (`rec_id`),
  KEY `idx_fld_type_id` (`fld_type_id`),
  KEY `idx_ioc_resource_id` (`ioc_resource_id`),
  CONSTRAINT `fld_ibfk_1` FOREIGN KEY (`rec_id`) REFERENCES `rec` (`rec_id`),
  CONSTRAINT `fld_ibfk_2` FOREIGN KEY (`fld_type_id`) REFERENCES `fld_type` (`fld_type_id`),
  CONSTRAINT `fld_ibfk_3` FOREIGN KEY (`ioc_resource_id`) REFERENCES `ioc_resource` (`ioc_resource_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fld`
--

LOCK TABLES `fld` WRITE;
/*!40000 ALTER TABLE `fld` DISABLE KEYS */;
/*!40000 ALTER TABLE `fld` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fld_type`
--

DROP TABLE IF EXISTS `fld_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fld_type` (
  `fld_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `rec_type_id` int(11) DEFAULT NULL,
  `fld_type` varchar(24) DEFAULT NULL,
  `dbd_type` varchar(24) DEFAULT NULL,
  `def_fld_val` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`fld_type_id`),
  KEY `idx_dbd_type` (`dbd_type`),
  KEY `idx_rec_type_id` (`rec_type_id`),
  CONSTRAINT `fld_type_ibfk_1` FOREIGN KEY (`rec_type_id`) REFERENCES `rec_type` (`rec_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fld_type`
--

LOCK TABLES `fld_type` WRITE;
/*!40000 ALTER TABLE `fld_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `fld_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gold_lattice`
--

DROP TABLE IF EXISTS `gold_lattice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gold_lattice` (
  `gold_lattice_id` int(11) NOT NULL AUTO_INCREMENT,
  `lattice_id` int(11) DEFAULT NULL,
  `created_by` varchar(45) DEFAULT NULL,
  `create_date` datetime DEFAULT NULL,
  `updated_by` varchar(45) DEFAULT NULL,
  `update_date` datetime DEFAULT NULL,
  `gold_status_ind` int(11) DEFAULT NULL,
  PRIMARY KEY (`gold_lattice_id`),
  KEY `FK_gold_lattice_id` (`lattice_id`),
  CONSTRAINT `FK_gold_lattice_id` FOREIGN KEY (`lattice_id`) REFERENCES `lattice` (`lattice_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gold_lattice`
--

LOCK TABLES `gold_lattice` WRITE;
/*!40000 ALTER TABLE `gold_lattice` DISABLE KEYS */;
/*!40000 ALTER TABLE `gold_lattice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gold_model`
--

DROP TABLE IF EXISTS `gold_model`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gold_model` (
  `gold_model_id` int(11) NOT NULL AUTO_INCREMENT,
  `model_id` int(11) DEFAULT NULL,
  `created_by` varchar(45) DEFAULT NULL,
  `create_date` datetime DEFAULT NULL,
  `updated_by` varchar(45) DEFAULT NULL,
  `update_date` datetime DEFAULT NULL,
  `gold_status_ind` int(11) DEFAULT NULL,
  PRIMARY KEY (`gold_model_id`),
  KEY `Ref_215` (`model_id`),
  CONSTRAINT `Ref_215` FOREIGN KEY (`model_id`) REFERENCES `model` (`model_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gold_model`
--

LOCK TABLES `gold_model` WRITE;
/*!40000 ALTER TABLE `gold_model` DISABLE KEYS */;
/*!40000 ALTER TABLE `gold_model` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hall_probe_data`
--

DROP TABLE IF EXISTS `hall_probe_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `hall_probe_data` (
  `hall_probe_id` int(11) NOT NULL AUTO_INCREMENT,
  `inventory_id` int(11) DEFAULT NULL,
  `alias` varchar(50) DEFAULT NULL,
  `meas_date` datetime DEFAULT NULL,
  `measured_at_location` varchar(50) DEFAULT NULL,
  `sub_device` varchar(50) NOT NULL DEFAULT '0',
  `run_identifier` varchar(50) DEFAULT NULL,
  `login_name` varchar(50) DEFAULT NULL,
  `conditioning_current` double DEFAULT NULL,
  `current_1` double DEFAULT NULL,
  `current_2` double DEFAULT NULL,
  `current_3` double DEFAULT NULL,
  `up_dn1` varchar(50) DEFAULT NULL,
  `up_dn2` varchar(50) DEFAULT NULL,
  `up_dn3` varchar(50) DEFAULT NULL,
  `mag_volt_1` double DEFAULT NULL,
  `mag_volt_2` double DEFAULT NULL,
  `mag_volt_3` double DEFAULT NULL,
  `x` double DEFAULT NULL,
  `y` double DEFAULT NULL,
  `z` double DEFAULT NULL,
  `bx_t` double DEFAULT NULL,
  `by_t` double DEFAULT NULL,
  `bz_t` double DEFAULT NULL,
  `meas_notes` varchar(255) DEFAULT NULL,
  `data_issues` varchar(255) DEFAULT NULL,
  `data_usage` int(11) DEFAULT NULL,
  PRIMARY KEY (`hall_probe_id`),
  KEY `Ref_165` (`inventory_id`),
  CONSTRAINT `Ref_165` FOREIGN KEY (`inventory_id`) REFERENCES `inventory` (`inventory_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hall_probe_data`
--

LOCK TABLES `hall_probe_data` WRITE;
/*!40000 ALTER TABLE `hall_probe_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `hall_probe_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `install`
--

DROP TABLE IF EXISTS `install`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `install` (
  `install_id` int(11) NOT NULL AUTO_INCREMENT,
  `cmpnt_type_id` int(11) NOT NULL DEFAULT '0',
  `field_name` varchar(255) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`install_id`),
  KEY `Ref_99` (`cmpnt_type_id`),
  CONSTRAINT `Ref_99` FOREIGN KEY (`cmpnt_type_id`) REFERENCES `cmpnt_type` (`cmpnt_type_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=1070 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `install`
--

LOCK TABLES `install` WRITE;
/*!40000 ALTER TABLE `install` DISABLE KEYS */;
INSERT INTO `install` VALUES (1,18,'FH1G1C30A','Storage Ring'),(2,18,'FH2G1C30A','Storage Ring'),(3,12,'SH1G2C30A','Storage Ring'),(4,7,'QH1G2C30A','Storage Ring'),(5,17,'SQHG2C30A','Storage Ring'),(6,5,'QH2G2C30A','Storage Ring'),(7,12,'SH3G2C30A','Storage Ring'),(8,7,'QH3G2C30A','Storage Ring'),(9,12,'SH4G2C30A','Storage Ring'),(10,15,'CH2G2C30A','Storage Ring'),(11,1,'B1G3C30A','Storage Ring'),(12,16,'CM1G4C30A','Storage Ring'),(13,4,'QM1G4C30A','Storage Ring'),(14,13,'SM1G4C30A','Storage Ring'),(15,18,'FM1G4C30A','Storage Ring'),(16,11,'QM2G4C30A','Storage Ring'),(17,14,'SM2G4C30B','Storage Ring'),(18,11,'QM2G4C30B','Storage Ring'),(19,12,'SM1G4C30B','Storage Ring'),(20,3,'QM1G4C30B','Storage Ring'),(21,15,'CM1G4C30B','Storage Ring'),(22,1,'B1G5C30B','Storage Ring'),(23,9,'QL3G6C30B','Storage Ring'),(24,13,'SL3G6C30B','Storage Ring'),(25,16,'CL2G6C30B','Storage Ring'),(26,6,'QL2G6C30B','Storage Ring'),(27,12,'SL2G6C30B','Storage Ring'),(28,16,'CL1G6C30B','Storage Ring'),(29,7,'QL1G6C30B','Storage Ring'),(30,12,'SL1G6C30B','Storage Ring'),(31,18,'FL1G1C01A','Storage Ring'),(32,18,'FL2G1C01A','Storage Ring'),(33,12,'SL1G2C01A','Storage Ring'),(34,7,'QL1G2C01A','Storage Ring'),(35,16,'CL1G2C01A','Storage Ring'),(36,12,'SL2G2C01A','Storage Ring'),(37,5,'QL2G2C01A','Storage Ring'),(38,16,'CL2G2C01A','Storage Ring'),(39,12,'SL3G2C01A','Storage Ring'),(40,7,'QL3G2C01A','Storage Ring'),(41,1,'B1G3C01A','Storage Ring'),(42,17,'SQMG4C01A','Storage Ring'),(43,4,'QM1G4C01A','Storage Ring'),(44,12,'SM1G4C01A','Storage Ring'),(45,18,'FM1G4C01A','Storage Ring'),(46,11,'QM2G4C01A','Storage Ring'),(47,14,'SM2G4C01B','Storage Ring'),(48,11,'QM2G4C01B','Storage Ring'),(49,12,'SM1G4C01B','Storage Ring'),(50,3,'QM1G4C01B','Storage Ring'),(51,15,'CM1G4C01B','Storage Ring'),(52,1,'B1G5C01B','Storage Ring'),(53,15,'CH2G6C01B','Storage Ring'),(54,13,'SH4G6C01B','Storage Ring'),(55,9,'QH3G6C01B','Storage Ring'),(56,13,'SH3G6C01B','Storage Ring'),(57,6,'QH2G6C01B','Storage Ring'),(58,16,'CH1G6C01B','Storage Ring'),(59,7,'QH1G6C01B','Storage Ring'),(60,12,'SH1G6C01B','Storage Ring'),(61,18,'FH1G1C02A','Storage Ring'),(62,18,'FH2G1C02A','Storage Ring'),(63,12,'SH1G2C02A','Storage Ring'),(64,7,'QH1G2C02A','Storage Ring'),(65,17,'SQHG2C02A','Storage Ring'),(66,5,'QH2G2C02A','Storage Ring'),(67,12,'SH3G2C02A','Storage Ring'),(68,7,'QH3G2C02A','Storage Ring'),(69,12,'SH4G2C02A','Storage Ring'),(70,15,'CH2G2C02A','Storage Ring'),(71,1,'B1G3C02A','Storage Ring'),(72,16,'CM1G4C02A','Storage Ring'),(73,4,'QM1G4C02A','Storage Ring'),(74,13,'SM1G4C02A','Storage Ring'),(75,18,'FM1G4C02A','Storage Ring'),(76,11,'QM2G4C02A','Storage Ring'),(77,14,'SM2G4C02B','Storage Ring'),(78,11,'QM2G4C02B','Storage Ring'),(79,12,'SM1G4C02B','Storage Ring'),(80,3,'QM1G4C02B','Storage Ring'),(81,15,'CM1G4C02B','Storage Ring'),(82,1,'B1G5C02B','Storage Ring'),(83,9,'QL3G6C02B','Storage Ring'),(84,13,'SL3G6C02B','Storage Ring'),(85,16,'CL2G6C02B','Storage Ring'),(86,6,'QL2G6C02B','Storage Ring'),(87,12,'SL2G6C02B','Storage Ring'),(88,16,'CL1G6C02B','Storage Ring'),(89,7,'QL1G6C02B','Storage Ring'),(90,12,'SL1G6C02B','Storage Ring'),(91,18,'FL1G1C03A','Storage Ring'),(92,18,'FL2G1C03A','Storage Ring'),(93,12,'SL1G2C03A','Storage Ring'),(94,7,'QL1G2C03A','Storage Ring'),(95,16,'CL1G2C03A','Storage Ring'),(96,12,'SL2G2C03A','Storage Ring'),(97,5,'QL2G2C03A','Storage Ring'),(98,16,'CL2G2C03A','Storage Ring'),(99,12,'SL3G2C03A','Storage Ring'),(100,7,'QL3G2C03A','Storage Ring'),(101,2,'B1G3C03A','Storage Ring'),(102,17,'SQMG4C03A','Storage Ring'),(103,4,'QM1G4C03A','Storage Ring'),(104,13,'SM1G4C03A','Storage Ring'),(105,18,'FM1G4C03A','Storage Ring'),(106,11,'QM2G4C03A','Storage Ring'),(107,14,'SM2G4C03B','Storage Ring'),(108,11,'QM2G4C03B','Storage Ring'),(109,12,'SM1G4C03B','Storage Ring'),(110,3,'QM1G4C03B','Storage Ring'),(111,15,'CM1G4C03B','Storage Ring'),(112,2,'B1G5C03B','Storage Ring'),(113,15,'CH2G6C03B','Storage Ring'),(114,13,'SH4G6C03B','Storage Ring'),(115,9,'QH3G6C03B','Storage Ring'),(116,13,'SH3G6C03B','Storage Ring'),(117,6,'QH2G6C03B','Storage Ring'),(118,16,'CH1G6C03B','Storage Ring'),(119,7,'QH1G6C03B','Storage Ring'),(120,12,'SH1G6C03B','Storage Ring'),(121,18,'FH1G1C04A','Storage Ring'),(122,18,'FH2G1C04A','Storage Ring'),(123,12,'SH1G2C04A','Storage Ring'),(124,7,'QH1G2C04A','Storage Ring'),(125,17,'SQHG2C04A','Storage Ring'),(126,5,'QH2G2C04A','Storage Ring'),(127,12,'SH3G2C04A','Storage Ring'),(128,7,'QH3G2C04A','Storage Ring'),(129,12,'SH4G2C04A','Storage Ring'),(130,15,'CH2G2C04A','Storage Ring'),(131,1,'B1G3C04A','Storage Ring'),(132,16,'CM1G4C04A','Storage Ring'),(133,4,'QM1G4C04A','Storage Ring'),(134,13,'SM1G4C04A','Storage Ring'),(135,18,'FM1G4C04A','Storage Ring'),(136,11,'QM2G4C04A','Storage Ring'),(137,14,'SM2G4C04B','Storage Ring'),(138,11,'QM2G4C04B','Storage Ring'),(139,12,'SM1G4C04B','Storage Ring'),(140,3,'QM1G4C04B','Storage Ring'),(141,15,'CM1G4C04B','Storage Ring'),(142,1,'B1G5C04B','Storage Ring'),(143,9,'QL3G6C04B','Storage Ring'),(144,13,'SL3G6C04B','Storage Ring'),(145,16,'CL2G6C04B','Storage Ring'),(146,6,'QL2G6C04B','Storage Ring'),(147,12,'SL2G6C04B','Storage Ring'),(148,16,'CL1G6C04B','Storage Ring'),(149,7,'QL1G6C04B','Storage Ring'),(150,12,'SL1G6C04B','Storage Ring'),(151,18,'FL1G1C05A','Storage Ring'),(152,18,'FL2G1C05A','Storage Ring'),(153,12,'SL1G2C05A','Storage Ring'),(154,7,'QL1G2C05A','Storage Ring'),(155,16,'CL1G2C05A','Storage Ring'),(156,12,'SL2G2C05A','Storage Ring'),(157,5,'QL2G2C05A','Storage Ring'),(158,16,'CL2G2C05A','Storage Ring'),(159,12,'SL3G2C05A','Storage Ring'),(160,7,'QL3G2C05A','Storage Ring'),(161,1,'B1G3C05A','Storage Ring'),(162,17,'SQMG4C05A','Storage Ring'),(163,4,'QM1G4C05A','Storage Ring'),(164,13,'SM1G4C05A','Storage Ring'),(165,18,'FM1G4C05A','Storage Ring'),(166,11,'QM2G4C05A','Storage Ring'),(167,14,'SM2G4C05B','Storage Ring'),(168,11,'QM2G4C05B','Storage Ring'),(169,12,'SM1G4C05B','Storage Ring'),(170,3,'QM1G4C05B','Storage Ring'),(171,15,'CM1G4C05B','Storage Ring'),(172,1,'B1G5C05B','Storage Ring'),(173,15,'CH2G6C05B','Storage Ring'),(174,13,'SH4G6C05B','Storage Ring'),(175,9,'QH3G6C05B','Storage Ring'),(176,13,'SH3G6C05B','Storage Ring'),(177,6,'QH2G6C05B','Storage Ring'),(178,16,'CH1G6C05B','Storage Ring'),(179,7,'QH1G6C05B','Storage Ring'),(180,12,'SH1G6C05B','Storage Ring'),(181,18,'FH1G1C06A','Storage Ring'),(182,18,'FH2G1C06A','Storage Ring'),(183,12,'SH1G2C06A','Storage Ring'),(184,7,'QH1G2C06A','Storage Ring'),(185,17,'SQHG2C06A','Storage Ring'),(186,5,'QH2G2C06A','Storage Ring'),(187,12,'SH3G2C06A','Storage Ring'),(188,7,'QH3G2C06A','Storage Ring'),(189,12,'SH4G2C06A','Storage Ring'),(190,15,'CH2G2C06A','Storage Ring'),(191,1,'B1G3C06A','Storage Ring'),(192,16,'CM1G4C06A','Storage Ring'),(193,4,'QM1G4C06A','Storage Ring'),(194,13,'SM1G4C06A','Storage Ring'),(195,18,'FM1G4C06A','Storage Ring'),(196,11,'QM2G4C06A','Storage Ring'),(197,14,'SM2G4C06B','Storage Ring'),(198,11,'QM2G4C06B','Storage Ring'),(199,12,'SM1G4C06B','Storage Ring'),(200,3,'QM1G4C06B','Storage Ring'),(201,15,'CM1G4C06B','Storage Ring'),(202,1,'B1G5C06B','Storage Ring'),(203,9,'QL3G6C06B','Storage Ring'),(204,13,'SL3G6C06B','Storage Ring'),(205,16,'CL2G6C06B','Storage Ring'),(206,6,'QL2G6C06B','Storage Ring'),(207,12,'SL2G6C06B','Storage Ring'),(208,16,'CL1G6C06B','Storage Ring'),(209,7,'QL1G6C06B','Storage Ring'),(210,12,'SL1G6C06B','Storage Ring'),(211,18,'FL1G1C07A','Storage Ring'),(212,18,'FL2G1C07A','Storage Ring'),(213,12,'SL1G2C07A','Storage Ring'),(214,7,'QL1G2C07A','Storage Ring'),(215,16,'CL1G2C07A','Storage Ring'),(216,12,'SL2G2C07A','Storage Ring'),(217,5,'QL2G2C07A','Storage Ring'),(218,16,'CL2G2C07A','Storage Ring'),(219,12,'SL3G2C07A','Storage Ring'),(220,7,'QL3G2C07A','Storage Ring'),(221,1,'B1G3C07A','Storage Ring'),(222,17,'SQMG4C07A','Storage Ring'),(223,4,'QM1G4C07A','Storage Ring'),(224,13,'SM1G4C07A','Storage Ring'),(225,18,'FM1G4C07A','Storage Ring'),(226,11,'QM2G4C07A','Storage Ring'),(227,14,'SM2G4C07B','Storage Ring'),(228,11,'QM2G4C07B','Storage Ring'),(229,12,'SM1G4C07B','Storage Ring'),(230,3,'QM1G4C07B','Storage Ring'),(231,15,'CM1G4C07B','Storage Ring'),(232,1,'B1G5C07B','Storage Ring'),(233,15,'CH2G6C07B','Storage Ring'),(234,13,'SH4G6C07B','Storage Ring'),(235,10,'QH3G6C07B','Storage Ring'),(236,13,'SH3G6C07B','Storage Ring'),(237,6,'QH2G6C07B','Storage Ring'),(238,16,'CH1G6C07B','Storage Ring'),(239,7,'QH1G6C07B','Storage Ring'),(240,12,'SH1G6C07B','Storage Ring'),(241,18,'FH1G1C08A','Storage Ring'),(242,18,'FH2G1C08A','Storage Ring'),(243,12,'SH1G2C08A','Storage Ring'),(244,7,'QH1G2C08A','Storage Ring'),(245,17,'SQHG2C08A','Storage Ring'),(246,5,'QH2G2C08A','Storage Ring'),(247,12,'SH3G2C08A','Storage Ring'),(248,8,'QH3G2C08A','Storage Ring'),(249,12,'SH4G2C08A','Storage Ring'),(250,15,'CH2G2C08A','Storage Ring'),(251,1,'B1G3C08A','Storage Ring'),(252,16,'CM1G4C08A','Storage Ring'),(253,4,'QM1G4C08A','Storage Ring'),(254,13,'SM1G4C08A','Storage Ring'),(255,18,'FM1G4C08A','Storage Ring'),(256,11,'QM2G4C08A','Storage Ring'),(257,14,'SM2G4C08B','Storage Ring'),(258,11,'QM2G4C08B','Storage Ring'),(259,12,'SM1G4C08B','Storage Ring'),(260,3,'QM1G4C08B','Storage Ring'),(261,15,'CM1G4C08B','Storage Ring'),(262,1,'B1G5C08B','Storage Ring'),(263,9,'QL3G6C08B','Storage Ring'),(264,13,'SL3G6C08B','Storage Ring'),(265,16,'CL2G6C08B','Storage Ring'),(266,6,'QL2G6C08B','Storage Ring'),(267,12,'SL2G6C08B','Storage Ring'),(268,16,'CL1G6C08B','Storage Ring'),(269,7,'QL1G6C08B','Storage Ring'),(270,12,'SL1G6C08B','Storage Ring'),(271,18,'FL1G1C09A','Storage Ring'),(272,18,'FL2G1C09A','Storage Ring'),(273,12,'SL1G2C09A','Storage Ring'),(274,7,'QL1G2C09A','Storage Ring'),(275,16,'CL1G2C09A','Storage Ring'),(276,12,'SL2G2C09A','Storage Ring'),(277,5,'QL2G2C09A','Storage Ring'),(278,16,'CL2G2C09A','Storage Ring'),(279,12,'SL3G2C09A','Storage Ring'),(280,7,'QL3G2C09A','Storage Ring'),(281,1,'B1G3C09A','Storage Ring'),(282,17,'SQMG4C09A','Storage Ring'),(283,4,'QM1G4C09A','Storage Ring'),(284,13,'SM1G4C09A','Storage Ring'),(285,18,'FM1G4C09A','Storage Ring'),(286,11,'QM2G4C09A','Storage Ring'),(287,14,'SM2G4C09B','Storage Ring'),(288,11,'QM2G4C09B','Storage Ring'),(289,12,'SM1G4C09B','Storage Ring'),(290,3,'QM1G4C09B','Storage Ring'),(291,15,'CM1G4C09B','Storage Ring'),(292,1,'B1G5C09B','Storage Ring'),(293,15,'CH2G6C09B','Storage Ring'),(294,13,'SH4G6C09B','Storage Ring'),(295,9,'QH3G6C09B','Storage Ring'),(296,13,'SH3G6C09B','Storage Ring'),(297,6,'QH2G6C09B','Storage Ring'),(298,16,'CH1G6C09B','Storage Ring'),(299,7,'QH1G6C09B','Storage Ring'),(300,12,'SH1G6C09B','Storage Ring'),(301,18,'FH1G1C10A','Storage Ring'),(302,18,'FH2G1C10A','Storage Ring'),(303,12,'SH1G2C10A','Storage Ring'),(304,7,'QH1G2C10A','Storage Ring'),(305,17,'SQHG2C10A','Storage Ring'),(306,5,'QH2G2C10A','Storage Ring'),(307,12,'SH3G2C10A','Storage Ring'),(308,7,'QH3G2C10A','Storage Ring'),(309,12,'SH4G2C10A','Storage Ring'),(310,15,'CH2G2C10A','Storage Ring'),(311,1,'B1G3C10A','Storage Ring'),(312,16,'CM1G4C10A','Storage Ring'),(313,4,'QM1G4C10A','Storage Ring'),(314,13,'SM1G4C10A','Storage Ring'),(315,18,'FM1G4C10A','Storage Ring'),(316,11,'QM2G4C10A','Storage Ring'),(317,14,'SM2G4C10B','Storage Ring'),(318,11,'QM2G4C10B','Storage Ring'),(319,12,'SM1G4C10B','Storage Ring'),(320,3,'QM1G4C10B','Storage Ring'),(321,15,'CM1G4C10B','Storage Ring'),(322,1,'B1G5C10B','Storage Ring'),(323,9,'QL3G6C10B','Storage Ring'),(324,13,'SL3G6C10B','Storage Ring'),(325,16,'CL2G6C10B','Storage Ring'),(326,6,'QL2G6C10B','Storage Ring'),(327,12,'SL2G6C10B','Storage Ring'),(328,16,'CL1G6C10B','Storage Ring'),(329,7,'QL1G6C10B','Storage Ring'),(330,12,'SL1G6C10B','Storage Ring'),(331,18,'FL1G1C11A','Storage Ring'),(332,18,'FL2G1C11A','Storage Ring'),(333,12,'SL1G2C11A','Storage Ring'),(334,7,'QL1G2C11A','Storage Ring'),(335,16,'CL1G2C11A','Storage Ring'),(336,12,'SL2G2C11A','Storage Ring'),(337,5,'QL2G2C11A','Storage Ring'),(338,16,'CL2G2C11A','Storage Ring'),(339,12,'SL3G2C11A','Storage Ring'),(340,7,'QL3G2C11A','Storage Ring'),(341,1,'B1G3C11A','Storage Ring'),(342,17,'SQMG4C11A','Storage Ring'),(343,4,'QM1G4C11A','Storage Ring'),(344,13,'SM1G4C11A','Storage Ring'),(345,18,'FM1G4C11A','Storage Ring'),(346,11,'QM2G4C11A','Storage Ring'),(347,14,'SM2G4C11B','Storage Ring'),(348,11,'QM2G4C11B','Storage Ring'),(349,12,'SM1G4C11B','Storage Ring'),(350,3,'QM1G4C11B','Storage Ring'),(351,15,'CM1G4C11B','Storage Ring'),(352,1,'B1G5C11B','Storage Ring'),(353,15,'CH2G6C11B','Storage Ring'),(354,13,'SH4G6C11B','Storage Ring'),(355,9,'QH3G6C11B','Storage Ring'),(356,13,'SH3G6C11B','Storage Ring'),(357,6,'QH2G6C11B','Storage Ring'),(358,16,'CH1G6C11B','Storage Ring'),(359,7,'QH1G6C11B','Storage Ring'),(360,12,'SH1G6C11B','Storage Ring'),(361,18,'FH1G1C12A','Storage Ring'),(362,18,'FH2G1C12A','Storage Ring'),(363,12,'SH1G2C12A','Storage Ring'),(364,7,'QH1G2C12A','Storage Ring'),(365,17,'SQHG2C12A','Storage Ring'),(366,5,'QH2G2C12A','Storage Ring'),(367,12,'SH3G2C12A','Storage Ring'),(368,7,'QH3G2C12A','Storage Ring'),(369,12,'SH4G2C12A','Storage Ring'),(370,15,'CH2G2C12A','Storage Ring'),(371,1,'B1G3C12A','Storage Ring'),(372,16,'CM1G4C12A','Storage Ring'),(373,4,'QM1G4C12A','Storage Ring'),(374,13,'SM1G4C12A','Storage Ring'),(375,18,'FM1G4C12A','Storage Ring'),(376,11,'QM2G4C12A','Storage Ring'),(377,14,'SM2G4C12B','Storage Ring'),(378,11,'QM2G4C12B','Storage Ring'),(379,12,'SM1G4C12B','Storage Ring'),(380,3,'QM1G4C12B','Storage Ring'),(381,15,'CM1G4C12B','Storage Ring'),(382,1,'B1G5C12B','Storage Ring'),(383,9,'QL3G6C12B','Storage Ring'),(384,13,'SL3G6C12B','Storage Ring'),(385,16,'CL2G6C12B','Storage Ring'),(386,6,'QL2G6C12B','Storage Ring'),(387,12,'SL2G6C12B','Storage Ring'),(388,16,'CL1G6C12B','Storage Ring'),(389,7,'QL1G6C12B','Storage Ring'),(390,12,'SL1G6C12B','Storage Ring'),(391,18,'FL1G1C13A','Storage Ring'),(392,18,'FL2G1C13A','Storage Ring'),(393,12,'SL1G2C13A','Storage Ring'),(394,7,'QL1G2C13A','Storage Ring'),(395,16,'CL1G2C13A','Storage Ring'),(396,12,'SL2G2C13A','Storage Ring'),(397,5,'QL2G2C13A','Storage Ring'),(398,16,'CL2G2C13A','Storage Ring'),(399,12,'SL3G2C13A','Storage Ring'),(400,7,'QL3G2C13A','Storage Ring'),(401,2,'B1G3C13A','Storage Ring'),(402,17,'SQMG4C13A','Storage Ring'),(403,4,'QM1G4C13A','Storage Ring'),(404,13,'SM1G4C13A','Storage Ring'),(405,18,'FM1G4C13A','Storage Ring'),(406,11,'QM2G4C13A','Storage Ring'),(407,14,'SM2G4C13B','Storage Ring'),(408,11,'QM2G4C13B','Storage Ring'),(409,12,'SM1G4C13B','Storage Ring'),(410,3,'QM1G4C13B','Storage Ring'),(411,15,'CM1G4C13B','Storage Ring'),(412,2,'B1G5C13B','Storage Ring'),(413,15,'CH2G6C13B','Storage Ring'),(414,13,'SH4G6C13B','Storage Ring'),(415,9,'QH3G6C13B','Storage Ring'),(416,13,'SH3G6C13B','Storage Ring'),(417,6,'QH2G6C13B','Storage Ring'),(418,16,'CH1G6C13B','Storage Ring'),(419,7,'QH1G6C13B','Storage Ring'),(420,12,'SH1G6C13B','Storage Ring'),(421,18,'FH1G1C14A','Storage Ring'),(422,18,'FH2G1C14A','Storage Ring'),(423,12,'SH1G2C14A','Storage Ring'),(424,7,'QH1G2C14A','Storage Ring'),(425,17,'SQHG2C14A','Storage Ring'),(426,5,'QH2G2C14A','Storage Ring'),(427,12,'SH3G2C14A','Storage Ring'),(428,7,'QH3G2C14A','Storage Ring'),(429,12,'SH4G2C14A','Storage Ring'),(430,15,'CH2G2C14A','Storage Ring'),(431,1,'B1G3C14A','Storage Ring'),(432,16,'CM1G4C14A','Storage Ring'),(433,4,'QM1G4C14A','Storage Ring'),(434,13,'SM1G4C14A','Storage Ring'),(435,18,'FM1G4C14A','Storage Ring'),(436,11,'QM2G4C14A','Storage Ring'),(437,14,'SM2G4C14B','Storage Ring'),(438,11,'QM2G4C14B','Storage Ring'),(439,12,'SM1G4C14B','Storage Ring'),(440,3,'QM1G4C14B','Storage Ring'),(441,15,'CM1G4C14B','Storage Ring'),(442,1,'B1G5C14B','Storage Ring'),(443,9,'QL3G6C14B','Storage Ring'),(444,13,'SL3G6C14B','Storage Ring'),(445,16,'CL2G6C14B','Storage Ring'),(446,6,'QL2G6C14B','Storage Ring'),(447,12,'SL2G6C14B','Storage Ring'),(448,16,'CL1G6C14B','Storage Ring'),(449,7,'QL1G6C14B','Storage Ring'),(450,12,'SL1G6C14B','Storage Ring'),(451,18,'FL1G1C15A','Storage Ring'),(452,18,'FL2G1C15A','Storage Ring'),(453,12,'SL1G2C15A','Storage Ring'),(454,7,'QL1G2C15A','Storage Ring'),(455,16,'CL1G2C15A','Storage Ring'),(456,12,'SL2G2C15A','Storage Ring'),(457,5,'QL2G2C15A','Storage Ring'),(458,16,'CL2G2C15A','Storage Ring'),(459,12,'SL3G2C15A','Storage Ring'),(460,7,'QL3G2C15A','Storage Ring'),(461,1,'B1G3C15A','Storage Ring'),(462,17,'SQMG4C15A','Storage Ring'),(463,4,'QM1G4C15A','Storage Ring'),(464,13,'SM1G4C15A','Storage Ring'),(465,18,'FM1G4C15A','Storage Ring'),(466,11,'QM2G4C15A','Storage Ring'),(467,14,'SM2G4C15B','Storage Ring'),(468,11,'QM2G4C15B','Storage Ring'),(469,12,'SM1G4C15B','Storage Ring'),(470,3,'QM1G4C15B','Storage Ring'),(471,15,'CM1G4C15B','Storage Ring'),(472,1,'B1G5C15B','Storage Ring'),(473,15,'CH2G6C15B','Storage Ring'),(474,13,'SH4G6C15B','Storage Ring'),(475,9,'QH3G6C15B','Storage Ring'),(476,13,'SH3G6C15B','Storage Ring'),(477,6,'QH2G6C15B','Storage Ring'),(478,16,'CH1G6C15B','Storage Ring'),(479,7,'QH1G6C15B','Storage Ring'),(480,12,'SH1G6C15B','Storage Ring'),(481,18,'FH1G1C16A','Storage Ring'),(482,18,'FH2G1C16A','Storage Ring'),(483,12,'SH1G2C16A','Storage Ring'),(484,7,'QH1G2C16A','Storage Ring'),(485,17,'SQHG2C16A','Storage Ring'),(486,5,'QH2G2C16A','Storage Ring'),(487,12,'SH3G2C16A','Storage Ring'),(488,7,'QH3G2C16A','Storage Ring'),(489,12,'SH4G2C16A','Storage Ring'),(490,15,'CH2G2C16A','Storage Ring'),(491,1,'B1G3C16A','Storage Ring'),(492,16,'CM1G4C16A','Storage Ring'),(493,4,'QM1G4C16A','Storage Ring'),(494,13,'SM1G4C16A','Storage Ring'),(495,18,'FM1G4C16A','Storage Ring'),(496,11,'QM2G4C16A','Storage Ring'),(497,14,'SM2G4C16B','Storage Ring'),(498,11,'QM2G4C16B','Storage Ring'),(499,12,'SM1G4C16B','Storage Ring'),(500,3,'QM1G4C16B','Storage Ring'),(501,15,'CM1G4C16B','Storage Ring'),(502,1,'B1G5C16B','Storage Ring'),(503,9,'QL3G6C16B','Storage Ring'),(504,13,'SL3G6C16B','Storage Ring'),(505,16,'CL2G6C16B','Storage Ring'),(506,6,'QL2G6C16B','Storage Ring'),(507,12,'SL2G6C16B','Storage Ring'),(508,16,'CL1G6C16B','Storage Ring'),(509,7,'QL1G6C16B','Storage Ring'),(510,12,'SL1G6C16B','Storage Ring'),(511,18,'FL1G1C17A','Storage Ring'),(512,18,'FL2G1C17A','Storage Ring'),(513,12,'SL1G2C17A','Storage Ring'),(514,7,'QL1G2C17A','Storage Ring'),(515,16,'CL1G2C17A','Storage Ring'),(516,12,'SL2G2C17A','Storage Ring'),(517,5,'QL2G2C17A','Storage Ring'),(518,16,'CL2G2C17A','Storage Ring'),(519,12,'SL3G2C17A','Storage Ring'),(520,7,'QL3G2C17A','Storage Ring'),(521,1,'B1G3C17A','Storage Ring'),(522,17,'SQMG4C17A','Storage Ring'),(523,4,'QM1G4C17A','Storage Ring'),(524,13,'SM1G4C17A','Storage Ring'),(525,18,'FM1G4C17A','Storage Ring'),(526,11,'QM2G4C17A','Storage Ring'),(527,14,'SM2G4C17B','Storage Ring'),(528,11,'QM2G4C17B','Storage Ring'),(529,12,'SM1G4C17B','Storage Ring'),(530,3,'QM1G4C17B','Storage Ring'),(531,15,'CM1G4C17B','Storage Ring'),(532,1,'B1G5C17B','Storage Ring'),(533,15,'CH2G6C17B','Storage Ring'),(534,13,'SH4G6C17B','Storage Ring'),(535,10,'QH3G6C17B','Storage Ring'),(536,13,'SH3G6C17B','Storage Ring'),(537,6,'QH2G6C17B','Storage Ring'),(538,16,'CH1G6C17B','Storage Ring'),(539,7,'QH1G6C17B','Storage Ring'),(540,12,'SH1G6C17B','Storage Ring'),(541,18,'FH1G1C18A','Storage Ring'),(542,18,'FH2G1C18A','Storage Ring'),(543,12,'SH1G2C18A','Storage Ring'),(544,7,'QH1G2C18A','Storage Ring'),(545,17,'SQHG2C18A','Storage Ring'),(546,5,'QH2G2C18A','Storage Ring'),(547,12,'SH3G2C18A','Storage Ring'),(548,8,'QH3G2C18A','Storage Ring'),(549,12,'SH4G2C18A','Storage Ring'),(550,15,'CH2G2C18A','Storage Ring'),(551,1,'B1G3C18A','Storage Ring'),(552,16,'CM1G4C18A','Storage Ring'),(553,4,'QM1G4C18A','Storage Ring'),(554,13,'SM1G4C18A','Storage Ring'),(555,18,'FM1G4C18A','Storage Ring'),(556,11,'QM2G4C18A','Storage Ring'),(557,14,'SM2G4C18B','Storage Ring'),(558,11,'QM2G4C18B','Storage Ring'),(559,12,'SM1G4C18B','Storage Ring'),(560,3,'QM1G4C18B','Storage Ring'),(561,15,'CM1G4C18B','Storage Ring'),(562,1,'B1G5C18B','Storage Ring'),(563,9,'QL3G6C18B','Storage Ring'),(564,13,'SL3G6C18B','Storage Ring'),(565,16,'CL2G6C18B','Storage Ring'),(566,6,'QL2G6C18B','Storage Ring'),(567,12,'SL2G6C18B','Storage Ring'),(568,16,'CL1G6C18B','Storage Ring'),(569,7,'QL1G6C18B','Storage Ring'),(570,12,'SL1G6C18B','Storage Ring'),(571,18,'FL1G1C19A','Storage Ring'),(572,18,'FL2G1C19A','Storage Ring'),(573,12,'SL1G2C19A','Storage Ring'),(574,7,'QL1G2C19A','Storage Ring'),(575,16,'CL1G2C19A','Storage Ring'),(576,12,'SL2G2C19A','Storage Ring'),(577,5,'QL2G2C19A','Storage Ring'),(578,16,'CL2G2C19A','Storage Ring'),(579,12,'SL3G2C19A','Storage Ring'),(580,7,'QL3G2C19A','Storage Ring'),(581,1,'B1G3C19A','Storage Ring'),(582,17,'SQMG4C19A','Storage Ring'),(583,4,'QM1G4C19A','Storage Ring'),(584,13,'SM1G4C19A','Storage Ring'),(585,18,'FM1G4C19A','Storage Ring'),(586,11,'QM2G4C19A','Storage Ring'),(587,14,'SM2G4C19B','Storage Ring'),(588,11,'QM2G4C19B','Storage Ring'),(589,12,'SM1G4C19B','Storage Ring'),(590,3,'QM1G4C19B','Storage Ring'),(591,15,'CM1G4C19B','Storage Ring'),(592,1,'B1G5C19B','Storage Ring'),(593,15,'CH2G6C19B','Storage Ring'),(594,13,'SH4G6C19B','Storage Ring'),(595,9,'QH3G6C19B','Storage Ring'),(596,13,'SH3G6C19B','Storage Ring'),(597,6,'QH2G6C19B','Storage Ring'),(598,16,'CH1G6C19B','Storage Ring'),(599,7,'QH1G6C19B','Storage Ring'),(600,12,'SH1G6C19B','Storage Ring'),(601,18,'FH1G1C20A','Storage Ring'),(602,18,'FH2G1C20A','Storage Ring'),(603,12,'SH1G2C20A','Storage Ring'),(604,7,'QH1G2C20A','Storage Ring'),(605,17,'SQHG2C20A','Storage Ring'),(606,5,'QH2G2C20A','Storage Ring'),(607,12,'SH3G2C20A','Storage Ring'),(608,7,'QH3G2C20A','Storage Ring'),(609,12,'SH4G2C20A','Storage Ring'),(610,15,'CH2G2C20A','Storage Ring'),(611,1,'B1G3C20A','Storage Ring'),(612,16,'CM1G4C20A','Storage Ring'),(613,4,'QM1G4C20A','Storage Ring'),(614,13,'SM1G4C20A','Storage Ring'),(615,18,'FM1G4C20A','Storage Ring'),(616,11,'QM2G4C20A','Storage Ring'),(617,14,'SM2G4C20B','Storage Ring'),(618,11,'QM2G4C20B','Storage Ring'),(619,12,'SM1G4C20B','Storage Ring'),(620,3,'QM1G4C20B','Storage Ring'),(621,15,'CM1G4C20B','Storage Ring'),(622,1,'B1G5C20B','Storage Ring'),(623,9,'QL3G6C20B','Storage Ring'),(624,13,'SL3G6C20B','Storage Ring'),(625,16,'CL2G6C20B','Storage Ring'),(626,6,'QL2G6C20B','Storage Ring'),(627,12,'SL2G6C20B','Storage Ring'),(628,16,'CL1G6C20B','Storage Ring'),(629,7,'QL1G6C20B','Storage Ring'),(630,12,'SL1G6C20B','Storage Ring'),(631,18,'FL1G1C21A','Storage Ring'),(632,18,'FL2G1C21A','Storage Ring'),(633,12,'SL1G2C21A','Storage Ring'),(634,7,'QL1G2C21A','Storage Ring'),(635,16,'CL1G2C21A','Storage Ring'),(636,12,'SL2G2C21A','Storage Ring'),(637,5,'QL2G2C21A','Storage Ring'),(638,16,'CL2G2C21A','Storage Ring'),(639,12,'SL3G2C21A','Storage Ring'),(640,7,'QL3G2C21A','Storage Ring'),(641,1,'B1G3C21A','Storage Ring'),(642,17,'SQMG4C21A','Storage Ring'),(643,4,'QM1G4C21A','Storage Ring'),(644,13,'SM1G4C21A','Storage Ring'),(645,18,'FM1G4C21A','Storage Ring'),(646,11,'QM2G4C21A','Storage Ring'),(647,14,'SM2G4C21B','Storage Ring'),(648,11,'QM2G4C21B','Storage Ring'),(649,12,'SM1G4C21B','Storage Ring'),(650,3,'QM1G4C21B','Storage Ring'),(651,15,'CM1G4C21B','Storage Ring'),(652,1,'B1G5C21B','Storage Ring'),(653,15,'CH2G6C21B','Storage Ring'),(654,13,'SH4G6C21B','Storage Ring'),(655,9,'QH3G6C21B','Storage Ring'),(656,13,'SH3G6C21B','Storage Ring'),(657,6,'QH2G6C21B','Storage Ring'),(658,16,'CH1G6C21B','Storage Ring'),(659,7,'QH1G6C21B','Storage Ring'),(660,12,'SH1G6C21B','Storage Ring'),(661,18,'FH1G1C22A','Storage Ring'),(662,18,'FH2G1C22A','Storage Ring'),(663,12,'SH1G2C22A','Storage Ring'),(664,7,'QH1G2C22A','Storage Ring'),(665,17,'SQHG2C22A','Storage Ring'),(666,5,'QH2G2C22A','Storage Ring'),(667,12,'SH3G2C22A','Storage Ring'),(668,7,'QH3G2C22A','Storage Ring'),(669,12,'SH4G2C22A','Storage Ring'),(670,15,'CH2G2C22A','Storage Ring'),(671,1,'B1G3C22A','Storage Ring'),(672,16,'CM1G4C22A','Storage Ring'),(673,4,'QM1G4C22A','Storage Ring'),(674,13,'SM1G4C22A','Storage Ring'),(675,18,'FM1G4C22A','Storage Ring'),(676,11,'QM2G4C22A','Storage Ring'),(677,14,'SM2G4C22B','Storage Ring'),(678,11,'QM2G4C22B','Storage Ring'),(679,12,'SM1G4C22B','Storage Ring'),(680,3,'QM1G4C22B','Storage Ring'),(681,15,'CM1G4C22B','Storage Ring'),(682,1,'B1G5C22B','Storage Ring'),(683,9,'QL3G6C22B','Storage Ring'),(684,13,'SL3G6C22B','Storage Ring'),(685,16,'CL2G6C22B','Storage Ring'),(686,6,'QL2G6C22B','Storage Ring'),(687,12,'SL2G6C22B','Storage Ring'),(688,16,'CL1G6C22B','Storage Ring'),(689,7,'QL1G6C22B','Storage Ring'),(690,12,'SL1G6C22B','Storage Ring'),(691,18,'FL1G1C23A','Storage Ring'),(692,18,'FL2G1C23A','Storage Ring'),(693,12,'SL1G2C23A','Storage Ring'),(694,7,'QL1G2C23A','Storage Ring'),(695,16,'CL1G2C23A','Storage Ring'),(696,12,'SL2G2C23A','Storage Ring'),(697,5,'QL2G2C23A','Storage Ring'),(698,16,'CL2G2C23A','Storage Ring'),(699,12,'SL3G2C23A','Storage Ring'),(700,7,'QL3G2C23A','Storage Ring'),(701,2,'B1G3C23A','Storage Ring'),(702,17,'SQMG4C23A','Storage Ring'),(703,4,'QM1G4C23A','Storage Ring'),(704,13,'SM1G4C23A','Storage Ring'),(705,18,'FM1G4C23A','Storage Ring'),(706,11,'QM2G4C23A','Storage Ring'),(707,14,'SM2G4C23B','Storage Ring'),(708,11,'QM2G4C23B','Storage Ring'),(709,12,'SM1G4C23B','Storage Ring'),(710,3,'QM1G4C23B','Storage Ring'),(711,15,'CM1G4C23B','Storage Ring'),(712,2,'B1G5C23B','Storage Ring'),(713,15,'CH2G6C23B','Storage Ring'),(714,13,'SH4G6C23B','Storage Ring'),(715,9,'QH3G6C23B','Storage Ring'),(716,13,'SH3G6C23B','Storage Ring'),(717,6,'QH2G6C23B','Storage Ring'),(718,16,'CH1G6C23B','Storage Ring'),(719,7,'QH1G6C23B','Storage Ring'),(720,12,'SH1G6C23B','Storage Ring'),(721,18,'FH1G1C24A','Storage Ring'),(722,18,'FH2G1C24A','Storage Ring'),(723,12,'SH1G2C24A','Storage Ring'),(724,7,'QH1G2C24A','Storage Ring'),(725,17,'SQHG2C24A','Storage Ring'),(726,5,'QH2G2C24A','Storage Ring'),(727,12,'SH3G2C24A','Storage Ring'),(728,7,'QH3G2C24A','Storage Ring'),(729,12,'SH4G2C24A','Storage Ring'),(730,15,'CH2G2C24A','Storage Ring'),(731,1,'B1G3C24A','Storage Ring'),(732,16,'CM1G4C24A','Storage Ring'),(733,4,'QM1G4C24A','Storage Ring'),(734,13,'SM1G4C24A','Storage Ring'),(735,18,'FM1G4C24A','Storage Ring'),(736,11,'QM2G4C24A','Storage Ring'),(737,14,'SM2G4C24B','Storage Ring'),(738,11,'QM2G4C24B','Storage Ring'),(739,12,'SM1G4C24B','Storage Ring'),(740,3,'QM1G4C24B','Storage Ring'),(741,15,'CM1G4C24B','Storage Ring'),(742,1,'B1G5C24B','Storage Ring'),(743,9,'QL3G6C24B','Storage Ring'),(744,13,'SL3G6C24B','Storage Ring'),(745,16,'CL2G6C24B','Storage Ring'),(746,6,'QL2G6C24B','Storage Ring'),(747,12,'SL2G6C24B','Storage Ring'),(748,16,'CL1G6C24B','Storage Ring'),(749,7,'QL1G6C24B','Storage Ring'),(750,12,'SL1G6C24B','Storage Ring'),(751,18,'FL1G1C25A','Storage Ring'),(752,18,'FL2G1C25A','Storage Ring'),(753,12,'SL1G2C25A','Storage Ring'),(754,7,'QL1G2C25A','Storage Ring'),(755,16,'CL1G2C25A','Storage Ring'),(756,12,'SL2G2C25A','Storage Ring'),(757,5,'QL2G2C25A','Storage Ring'),(758,16,'CL2G2C25A','Storage Ring'),(759,12,'SL3G2C25A','Storage Ring'),(760,7,'QL3G2C25A','Storage Ring'),(761,1,'B1G3C25A','Storage Ring'),(762,17,'SQMG4C25A','Storage Ring'),(763,4,'QM1G4C25A','Storage Ring'),(764,13,'SM1G4C25A','Storage Ring'),(765,18,'FM1G4C25A','Storage Ring'),(766,11,'QM2G4C25A','Storage Ring'),(767,14,'SM2G4C25B','Storage Ring'),(768,11,'QM2G4C25B','Storage Ring'),(769,12,'SM1G4C25B','Storage Ring'),(770,3,'QM1G4C25B','Storage Ring'),(771,15,'CM1G4C25B','Storage Ring'),(772,1,'B1G5C25B','Storage Ring'),(773,15,'CH2G6C25B','Storage Ring'),(774,13,'SH4G6C25B','Storage Ring'),(775,9,'QH3G6C25B','Storage Ring'),(776,13,'SH3G6C25B','Storage Ring'),(777,6,'QH2G6C25B','Storage Ring'),(778,16,'CH1G6C25B','Storage Ring'),(779,7,'QH1G6C25B','Storage Ring'),(780,12,'SH1G6C25B','Storage Ring'),(781,18,'FH1G1C26A','Storage Ring'),(782,18,'FH2G1C26A','Storage Ring'),(783,12,'SH1G2C26A','Storage Ring'),(784,7,'QH1G2C26A','Storage Ring'),(785,17,'SQHG2C26A','Storage Ring'),(786,5,'QH2G2C26A','Storage Ring'),(787,12,'SH3G2C26A','Storage Ring'),(788,7,'QH3G2C26A','Storage Ring'),(789,12,'SH4G2C26A','Storage Ring'),(790,15,'CH2G2C26A','Storage Ring'),(791,1,'B1G3C26A','Storage Ring'),(792,16,'CM1G4C26A','Storage Ring'),(793,4,'QM1G4C26A','Storage Ring'),(794,13,'SM1G4C26A','Storage Ring'),(795,18,'FM1G4C26A','Storage Ring'),(796,11,'QM2G4C26A','Storage Ring'),(797,14,'SM2G4C26B','Storage Ring'),(798,11,'QM2G4C26B','Storage Ring'),(799,12,'SM1G4C26B','Storage Ring'),(800,3,'QM1G4C26B','Storage Ring'),(801,15,'CM1G4C26B','Storage Ring'),(802,1,'B1G5C26B','Storage Ring'),(803,9,'QL3G6C26B','Storage Ring'),(804,13,'SL3G6C26B','Storage Ring'),(805,16,'CL2G6C26B','Storage Ring'),(806,6,'QL2G6C26B','Storage Ring'),(807,12,'SL2G6C26B','Storage Ring'),(808,16,'CL1G6C26B','Storage Ring'),(809,7,'QL1G6C26B','Storage Ring'),(810,12,'SL1G6C26B','Storage Ring'),(811,18,'FL1G1C27A','Storage Ring'),(812,18,'FL2G1C27A','Storage Ring'),(813,12,'SL1G2C27A','Storage Ring'),(814,7,'QL1G2C27A','Storage Ring'),(815,16,'CL1G2C27A','Storage Ring'),(816,12,'SL2G2C27A','Storage Ring'),(817,5,'QL2G2C27A','Storage Ring'),(818,16,'CL2G2C27A','Storage Ring'),(819,12,'SL3G2C27A','Storage Ring'),(820,7,'QL3G2C27A','Storage Ring'),(821,1,'B1G3C27A','Storage Ring'),(822,17,'SQMG4C27A','Storage Ring'),(823,4,'QM1G4C27A','Storage Ring'),(824,13,'SM1G4C27A','Storage Ring'),(825,18,'FM1G4C27A','Storage Ring'),(826,11,'QM2G4C27A','Storage Ring'),(827,14,'SM2G4C27B','Storage Ring'),(828,11,'QM2G4C27B','Storage Ring'),(829,12,'SM1G4C27B','Storage Ring'),(830,3,'QM1G4C27B','Storage Ring'),(831,15,'CM1G4C27B','Storage Ring'),(832,1,'B1G5C27B','Storage Ring'),(833,15,'CH2G6C27B','Storage Ring'),(834,13,'SH4G6C27B','Storage Ring'),(835,10,'QH3G6C27B','Storage Ring'),(836,13,'SH3G6C27B','Storage Ring'),(837,6,'QH2G6C27B','Storage Ring'),(838,16,'CH1G6C27B','Storage Ring'),(839,7,'QH1G6C27B','Storage Ring'),(840,12,'SH1G6C27B','Storage Ring'),(841,18,'FH1G1C28A','Storage Ring'),(842,18,'FH2G1C28A','Storage Ring'),(843,12,'SH1G2C28A','Storage Ring'),(844,7,'QH1G2C28A','Storage Ring'),(845,17,'SQHG2C28A','Storage Ring'),(846,5,'QH2G2C28A','Storage Ring'),(847,12,'SH3G2C28A','Storage Ring'),(848,8,'QH3G2C28A','Storage Ring'),(849,12,'SH4G2C28A','Storage Ring'),(850,15,'CH2G2C28A','Storage Ring'),(851,1,'B1G3C28A','Storage Ring'),(852,16,'CM1G4C28A','Storage Ring'),(853,4,'QM1G4C28A','Storage Ring'),(854,13,'SM1G4C28A','Storage Ring'),(855,18,'FM1G4C28A','Storage Ring'),(856,11,'QM2G4C28A','Storage Ring'),(857,14,'SM2G4C28B','Storage Ring'),(858,11,'QM2G4C28B','Storage Ring'),(859,12,'SM1G4C28B','Storage Ring'),(860,3,'QM1G4C28B','Storage Ring'),(861,15,'CM1G4C28B','Storage Ring'),(862,1,'B1G5C28B','Storage Ring'),(863,9,'QL3G6C28B','Storage Ring'),(864,13,'SL3G6C28B','Storage Ring'),(865,16,'CL2G6C28B','Storage Ring'),(866,6,'QL2G6C28B','Storage Ring'),(867,12,'SL2G6C28B','Storage Ring'),(868,16,'CL1G6C28B','Storage Ring'),(869,7,'QL1G6C28B','Storage Ring'),(870,12,'SL1G6C28B','Storage Ring'),(871,18,'FL1G1C29A','Storage Ring'),(872,18,'FL2G1C29A','Storage Ring'),(873,12,'SL1G2C29A','Storage Ring'),(874,7,'QL1G2C29A','Storage Ring'),(875,16,'CL1G2C29A','Storage Ring'),(876,12,'SL2G2C29A','Storage Ring'),(877,5,'QL2G2C29A','Storage Ring'),(878,16,'CL2G2C29A','Storage Ring'),(879,12,'SL3G2C29A','Storage Ring'),(880,7,'QL3G2C29A','Storage Ring'),(881,1,'B1G3C29A','Storage Ring'),(882,17,'SQMG4C29A','Storage Ring'),(883,4,'QM1G4C29A','Storage Ring'),(884,13,'SM1G4C29A','Storage Ring'),(885,18,'FM1G4C29A','Storage Ring'),(886,11,'QM2G4C29A','Storage Ring'),(887,14,'SM2G4C29B','Storage Ring'),(888,11,'QM2G4C29B','Storage Ring'),(889,12,'SM1G4C29B','Storage Ring'),(890,3,'QM1G4C29B','Storage Ring'),(891,15,'CM1G4C29B','Storage Ring'),(892,1,'B1G5C29B','Storage Ring'),(893,15,'CH2G6C29B','Storage Ring'),(894,13,'SH4G6C29B','Storage Ring'),(895,9,'QH3G6C29B','Storage Ring'),(896,13,'SH3G6C29B','Storage Ring'),(897,6,'QH2G6C29B','Storage Ring'),(898,16,'CH1G6C29B','Storage Ring'),(899,7,'QH1G6C29B','Storage Ring'),(900,12,'SH1G6C29B','Storage Ring'),(901,27,'LN-SO2','Linac'),(902,27,'LN-SO3','Linac'),(903,27,'LN-SO4','Linac'),(904,27,'LN-SO5','Linac'),(905,27,'LN-SO6','Linac'),(906,27,'LN-SO7','Linac'),(907,27,'LN-SO8','Linac'),(908,27,'LN-SO9','Linac'),(909,27,'LN-SO10','Linac'),(910,27,'LN-SO11','Linac'),(911,27,'LN-SO12','Linac'),(912,27,'LN-SO13','Linac'),(913,27,'LN-SO14','Linac'),(914,27,'LN-SO15','Linac'),(915,27,'LN-SO16','Linac'),(916,27,'LN-SO17','Linac'),(917,27,'LN-SO18','Linac'),(918,27,'LN-SO19','Linac'),(919,27,'LN-SO20','Linac'),(920,28,'LN-Q1','Linac'),(921,28,'LN-Q2','Linac'),(922,28,'LN-Q3','Linac'),(923,28,'LN-Q4','Linac'),(924,28,'LN-Q5','Linac'),(925,28,'LN-Q6','Linac'),(926,28,'LN-Q7','Linac'),(927,28,'LN-Q8','Linac'),(928,28,'LN-Q9','Linac'),(929,29,'LB-B1','LBT'),(930,29,'LB-B2','LBT'),(931,29,'LB-B3','LBT'),(932,29,'LB-B4','LBT'),(933,30,'LB-Q5','LBT'),(934,30,'LB-Q6','LBT'),(935,31,'LB-Q1','LBT'),(936,31,'LB-Q2','LBT'),(937,31,'LB-Q3','LBT'),(938,31,'LB-Q4','LBT'),(939,31,'LB-Q7','LBT'),(940,31,'LB-Q8','LBT'),(941,31,'LB-Q9','LBT'),(942,31,'LB-Q10','LBT'),(943,31,'LB-Q11','LBT'),(944,31,'LB-Q12','LBT'),(945,31,'LB-Q13','LBT'),(946,31,'LB-Q14','LBT'),(947,31,'LB-Q15','LBT'),(948,31,'LB-Q1BD1','LBT'),(949,31,'LB-Q2BD1','LBT'),(950,32,'A1BD1','Booster'),(951,32,'A1BD2','Booster'),(952,32,'A1BD3','Booster'),(953,32,'A1BD4','Booster'),(954,32,'A1BD5','Booster'),(955,32,'A1BD6','Booster'),(956,32,'A1BD7','Booster'),(957,32,'A1BD8','Booster'),(958,32,'A2BD1','Booster'),(959,32,'A2BD2','Booster'),(960,32,'A2BD3','Booster'),(961,32,'A2BD4','Booster'),(962,32,'A2BD5','Booster'),(963,32,'A2BD6','Booster'),(964,32,'A2BD7','Booster'),(965,32,'A2BD8','Booster'),(966,33,'A3BD1','Booster'),(967,33,'A3BD2','Booster'),(968,33,'A3BD3','Booster'),(969,33,'A3BD4','Booster'),(970,33,'A3BD5','Booster'),(971,33,'A3BD6','Booster'),(972,33,'A3BD7','Booster'),(973,33,'A3BD8','Booster'),(974,33,'A4BD1','Booster'),(975,33,'A4BD2','Booster'),(976,33,'A4BD3','Booster'),(977,33,'A4BD4','Booster'),(978,33,'A4BD5','Booster'),(979,33,'A4BD6','Booster'),(980,33,'A4BD7','Booster'),(981,33,'A4BD8','Booster'),(982,34,'A1BF1','Booster'),(983,34,'A1BF2','Booster'),(984,34,'A1BF3','Booster'),(985,34,'A1BF4','Booster'),(986,34,'A1BF5','Booster'),(987,34,'A1BF6','Booster'),(988,34,'A1BF7','Booster'),(989,34,'A2BF1','Booster'),(990,34,'A2BF2','Booster'),(991,34,'A2BF3','Booster'),(992,34,'A2BF4','Booster'),(993,34,'A2BF5','Booster'),(994,34,'A2BF6','Booster'),(995,34,'A2BF7','Booster'),(996,34,'A3BF1','Booster'),(997,34,'A3BF2','Booster'),(998,34,'A3BF3','Booster'),(999,34,'A3BF4','Booster'),(1000,34,'A3BF5','Booster'),(1001,34,'A3BF6','Booster'),(1002,34,'A3BF7','Booster'),(1003,34,'A4BF1','Booster'),(1004,34,'A4BF2','Booster'),(1005,34,'A4BF3','Booster'),(1006,34,'A4BF4','Booster'),(1007,34,'A4BF5','Booster'),(1008,34,'A4BF6','Booster'),(1009,34,'A4BF7','Booster'),(1010,35,'A1QF1','Booster'),(1011,35,'A1QF2','Booster'),(1012,35,'A2QF1','Booster'),(1013,35,'A2QF2','Booster'),(1014,35,'A3QF1','Booster'),(1015,35,'A3QF2','Booster'),(1016,35,'A4QF1','Booster'),(1017,35,'A4QF2','Booster'),(1018,36,'A1QD1','Booster'),(1019,36,'A1QD2','Booster'),(1020,36,'A2QD1','Booster'),(1021,36,'A2QD2','Booster'),(1022,36,'A3QD1','Booster'),(1023,36,'A3QD2','Booster'),(1024,36,'A4QD1','Booster'),(1025,36,'A4QD2','Booster'),(1026,37,'A1QG1','Booster'),(1027,37,'A1QG2','Booster'),(1028,37,'A2QG1','Booster'),(1029,37,'A2QG2','Booster'),(1030,37,'A3QG1','Booster'),(1031,37,'A3QG2','Booster'),(1032,37,'A4QG1','Booster'),(1033,37,'A4QG2','Booster'),(1034,38,'A1SF1','Booster'),(1035,38,'A1SF2','Booster'),(1036,38,'A2SF1','Booster'),(1037,38,'A2SF2','Booster'),(1038,38,'A3SF1','Booster'),(1039,38,'A3SF2','Booster'),(1040,38,'A4SF1','Booster'),(1041,38,'A4SF2','Booster'),(1042,39,'A1SD1','Booster'),(1043,39,'A1SD2','Booster'),(1044,39,'A2SD1','Booster'),(1045,39,'A2SD2','Booster'),(1046,39,'A3SD1','Booster'),(1047,39,'A3SD2','Booster'),(1048,39,'A4SD1','Booster'),(1049,39,'A4SD2','Booster'),(1050,40,'BS-B1','BST'),(1051,40,'BS-B2','BST'),(1052,40,'BS-B3','BST'),(1053,40,'BS-B4','BST'),(1054,41,'BS-Q1','BST'),(1055,41,'BS-Q2','BST'),(1056,41,'BS-Q3','BST'),(1057,41,'BS-Q4','BST'),(1058,41,'BS-Q5','BST'),(1059,41,'BS-Q6','BST'),(1060,41,'BS-Q7','BST'),(1061,41,'BS-Q8','BST'),(1062,41,'BS-Q9','BST'),(1063,41,'BS-Q10','BST'),(1064,41,'BS-Q11','BST'),(1065,41,'BS-Q12','BST'),(1066,41,'BS-Q13','BST'),(1067,41,'BS-Q14','BST'),(1068,41,'BS-Q1BD1','BST'),(1069,41,'BS-Q2BD1','BST');
/*!40000 ALTER TABLE `install` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `install__document`
--

DROP TABLE IF EXISTS `install__document`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `install__document` (
  `install__document_id` int(11) NOT NULL AUTO_INCREMENT,
  `install_id` int(11) DEFAULT NULL,
  `document_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`install__document_id`),
  KEY `Ref_252` (`document_id`),
  KEY `Ref_253` (`install_id`),
  CONSTRAINT `Ref_252` FOREIGN KEY (`document_id`) REFERENCES `document` (`document_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Ref_253` FOREIGN KEY (`install_id`) REFERENCES `install` (`install_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `install__document`
--

LOCK TABLES `install__document` WRITE;
/*!40000 ALTER TABLE `install__document` DISABLE KEYS */;
/*!40000 ALTER TABLE `install__document` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `install_partition_type`
--

DROP TABLE IF EXISTS `install_partition_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `install_partition_type` (
  `install_partition_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `install_id` int(11) DEFAULT NULL,
  `partition_type_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`install_partition_type_id`),
  KEY `Ref_150` (`install_id`),
  KEY `Ref_152` (`partition_type_id`),
  CONSTRAINT `Ref_150` FOREIGN KEY (`install_id`) REFERENCES `install` (`install_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Ref_152` FOREIGN KEY (`partition_type_id`) REFERENCES `partition_type` (`partition_type_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `install_partition_type`
--

LOCK TABLES `install_partition_type` WRITE;
/*!40000 ALTER TABLE `install_partition_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `install_partition_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `install_rel`
--

DROP TABLE IF EXISTS `install_rel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `install_rel` (
  `install_rel_id` int(11) NOT NULL AUTO_INCREMENT,
  `install_rel_type_id` int(11) DEFAULT NULL,
  `parent_install_id` int(11) NOT NULL DEFAULT '0',
  `child_install_id` int(11) NOT NULL DEFAULT '0',
  `logical_desc` varchar(60) DEFAULT NULL,
  `logical_order` int(11) DEFAULT NULL,
  `install_date` datetime DEFAULT NULL,
  PRIMARY KEY (`install_rel_id`),
  KEY `idx_cmpnt_rel_type_id` (`install_rel_type_id`),
  KEY `Ref_100` (`parent_install_id`),
  KEY `Ref_101` (`child_install_id`),
  CONSTRAINT `cmpnt_rel_ibfk_3` FOREIGN KEY (`install_rel_type_id`) REFERENCES `install_rel_type` (`install_rel_type_id`),
  CONSTRAINT `Ref_100` FOREIGN KEY (`parent_install_id`) REFERENCES `install` (`install_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Ref_101` FOREIGN KEY (`child_install_id`) REFERENCES `install` (`install_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `install_rel`
--

LOCK TABLES `install_rel` WRITE;
/*!40000 ALTER TABLE `install_rel` DISABLE KEYS */;
/*!40000 ALTER TABLE `install_rel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `install_rel_prop`
--

DROP TABLE IF EXISTS `install_rel_prop`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `install_rel_prop` (
  `install_rel__prop_id` int(11) NOT NULL AUTO_INCREMENT,
  `install_rel_id` int(11) DEFAULT NULL,
  `install_rel_prop_type_id` int(11) DEFAULT NULL,
  `install_rel_prop_value` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`install_rel__prop_id`),
  KEY `Ref_184` (`install_rel_id`),
  KEY `Ref_208` (`install_rel_prop_type_id`),
  CONSTRAINT `Ref_184` FOREIGN KEY (`install_rel_id`) REFERENCES `install_rel` (`install_rel_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Ref_208` FOREIGN KEY (`install_rel_prop_type_id`) REFERENCES `install_rel_prop_type` (`install_rel_prop_type_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `install_rel_prop`
--

LOCK TABLES `install_rel_prop` WRITE;
/*!40000 ALTER TABLE `install_rel_prop` DISABLE KEYS */;
/*!40000 ALTER TABLE `install_rel_prop` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `install_rel_prop_type`
--

DROP TABLE IF EXISTS `install_rel_prop_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `install_rel_prop_type` (
  `install_rel_prop_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `install_rel_prop_type_name` varchar(50) DEFAULT NULL,
  `install_rel_prop_type_desc` varchar(50) DEFAULT NULL,
  `install_rel_prop_type_units` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`install_rel_prop_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 PACK_KEYS=1 CHECKSUM=1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `install_rel_prop_type`
--

LOCK TABLES `install_rel_prop_type` WRITE;
/*!40000 ALTER TABLE `install_rel_prop_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `install_rel_prop_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `install_rel_type`
--

DROP TABLE IF EXISTS `install_rel_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `install_rel_type` (
  `install_rel_type_id` int(11) NOT NULL,
  `rel_name` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`install_rel_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `install_rel_type`
--

LOCK TABLES `install_rel_type` WRITE;
/*!40000 ALTER TABLE `install_rel_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `install_rel_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interface`
--

DROP TABLE IF EXISTS `interface`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `interface` (
  `interface_id` int(11) NOT NULL AUTO_INCREMENT,
  `install_rel_type_id` int(11) NOT NULL,
  `interface` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`interface_id`),
  UNIQUE KEY `idx_interface_cmpnt_rel_type` (`install_rel_type_id`,`interface`),
  KEY `idx_cmpnt_rel_type_id` (`install_rel_type_id`),
  CONSTRAINT `cmpntreltype__interface_ibfk_1` FOREIGN KEY (`install_rel_type_id`) REFERENCES `install_rel_type` (`install_rel_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interface`
--

LOCK TABLES `interface` WRITE;
/*!40000 ALTER TABLE `interface` DISABLE KEYS */;
/*!40000 ALTER TABLE `interface` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventory`
--

DROP TABLE IF EXISTS `inventory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `inventory` (
  `inventory_id` int(11) NOT NULL AUTO_INCREMENT,
  `cmpnt_type_id` int(11) NOT NULL,
  `vendor_id` int(11) DEFAULT NULL,
  `serial_no` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`inventory_id`),
  KEY `idx_cmpnt_type_id_c` (`cmpnt_type_id`),
  KEY `Ref_244` (`vendor_id`),
  CONSTRAINT `cmpnt_ibfk_1` FOREIGN KEY (`cmpnt_type_id`) REFERENCES `cmpnt_type` (`cmpnt_type_id`),
  CONSTRAINT `Ref_244` FOREIGN KEY (`vendor_id`) REFERENCES `vendor` (`vendor_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=801 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory`
--

LOCK TABLES `inventory` WRITE;
/*!40000 ALTER TABLE `inventory` DISABLE KEYS */;
INSERT INTO `inventory` VALUES (1,16,1,'1'),(2,16,1,'2'),(3,16,1,'3'),(4,16,1,'4'),(5,16,1,'6'),(6,16,1,'9'),(7,16,1,'12'),(8,16,1,'13'),(9,16,1,'31'),(10,17,1,'1'),(11,17,1,'2'),(12,17,1,'3'),(13,17,1,'4'),(14,17,1,'5'),(15,17,1,'6'),(16,17,1,'7'),(17,17,1,'8'),(18,17,1,'9'),(19,17,1,'10'),(20,17,1,'11'),(21,17,1,'12'),(22,17,1,'13'),(23,17,1,'14'),(24,17,1,'15'),(25,17,1,'16'),(26,17,1,'17'),(27,17,1,'18'),(28,17,1,'19'),(29,17,1,'20'),(30,17,1,'21'),(31,17,1,'22'),(32,17,1,'23'),(33,17,1,'24'),(34,17,1,'25'),(35,17,1,'26'),(36,17,1,'27'),(37,17,1,'28'),(38,17,1,'29'),(39,17,1,'30'),(40,15,1,'3'),(41,3,2,'1'),(42,3,2,'2'),(43,3,2,'3'),(44,3,2,'4'),(45,3,2,'5'),(46,3,2,'6'),(47,3,2,'7'),(48,3,2,'8'),(49,3,2,'9'),(50,3,2,'10'),(51,3,2,'11'),(52,3,2,'12'),(53,3,2,'13'),(54,3,2,'14'),(55,3,2,'15'),(56,3,2,'16'),(57,3,2,'17'),(58,3,2,'18'),(59,3,2,'19'),(60,3,2,'20'),(61,3,2,'21'),(62,3,2,'22'),(63,3,2,'23'),(64,3,2,'24'),(65,3,2,'25'),(66,3,2,'26'),(67,3,2,'27'),(68,3,2,'28'),(69,3,2,'29'),(70,3,2,'30'),(71,5,2,'1'),(72,5,2,'2'),(73,5,2,'3'),(74,5,2,'4'),(75,5,2,'5'),(76,5,2,'6'),(77,5,2,'7'),(78,5,2,'8'),(79,5,2,'9'),(80,5,2,'10'),(81,5,2,'11'),(82,5,2,'12'),(83,5,2,'13'),(84,5,2,'14'),(85,5,2,'15'),(86,5,2,'16'),(87,5,2,'17'),(88,5,2,'18'),(89,5,2,'19'),(90,5,2,'20'),(91,5,2,'21'),(92,5,2,'22'),(93,5,2,'23'),(94,5,2,'24'),(95,5,2,'25'),(96,5,2,'26'),(97,5,2,'27'),(98,5,2,'28'),(99,5,2,'29'),(100,5,2,'30'),(101,6,2,'2'),(102,6,2,'3'),(103,6,2,'4'),(104,6,2,'5'),(105,6,2,'6'),(106,6,2,'7'),(107,6,2,'8'),(108,6,2,'9'),(109,6,2,'10'),(110,6,2,'11'),(111,6,2,'12'),(112,6,2,'13'),(113,6,2,'14'),(114,6,2,'15'),(115,6,2,'16'),(116,6,2,'17'),(117,6,2,'18'),(118,6,2,'19'),(119,6,2,'20'),(120,6,2,'21'),(121,6,2,'22'),(122,6,2,'23'),(123,6,2,'24'),(124,6,2,'25'),(125,6,2,'26'),(126,6,2,'27'),(127,6,2,'28'),(128,6,2,'29'),(129,6,2,'30'),(130,6,2,'31'),(131,7,3,'1'),(132,7,3,'3'),(133,7,3,'4'),(134,7,3,'5'),(135,7,3,'6'),(136,7,3,'7'),(137,7,3,'8'),(138,7,3,'9'),(139,7,3,'10'),(140,7,3,'11'),(141,7,3,'12'),(142,7,3,'13'),(143,7,3,'14'),(144,7,3,'15'),(145,7,3,'16'),(146,7,3,'17'),(147,7,3,'18'),(148,7,3,'19'),(149,7,3,'20'),(150,7,3,'21'),(151,7,3,'22'),(152,7,3,'23'),(153,7,3,'24'),(154,7,3,'25'),(155,7,3,'26'),(156,7,3,'27'),(157,7,3,'28'),(158,7,3,'29'),(159,7,3,'30'),(160,7,3,'31'),(161,7,3,'32'),(162,7,3,'33'),(163,7,3,'34'),(164,7,3,'35'),(165,7,3,'36'),(166,7,3,'37'),(167,7,3,'38'),(168,7,3,'39'),(169,7,3,'40'),(170,7,3,'41'),(171,7,3,'42'),(172,7,3,'43'),(173,7,3,'44'),(174,7,3,'45'),(175,7,3,'46'),(176,7,3,'47'),(177,7,3,'48'),(178,7,3,'49'),(179,7,3,'50'),(180,7,3,'51'),(181,7,3,'52'),(182,7,3,'53'),(183,7,3,'54'),(184,7,3,'55'),(185,7,3,'56'),(186,7,3,'57'),(187,7,3,'58'),(188,7,3,'59'),(189,7,3,'60'),(190,7,3,'61'),(191,7,3,'62'),(192,7,3,'63'),(193,7,3,'64'),(194,7,3,'65'),(195,7,3,'66'),(196,7,3,'67'),(197,7,3,'68'),(198,7,3,'69'),(199,7,3,'70'),(200,7,3,'71'),(201,7,3,'72'),(202,7,3,'73'),(203,7,3,'74'),(204,7,3,'75'),(205,7,3,'76'),(206,7,3,'77'),(207,7,3,'78'),(208,7,3,'79'),(209,7,3,'80'),(210,7,3,'81'),(211,7,3,'82'),(212,7,3,'83'),(213,7,3,'84'),(214,7,3,'85'),(215,7,3,'86'),(216,7,3,'87'),(217,7,3,'88'),(218,7,3,'89'),(219,7,3,'90'),(220,7,3,'91'),(221,8,2,'1'),(222,8,2,'1002'),(223,8,2,'1003'),(224,11,4,'1'),(225,11,4,'2'),(226,11,4,'3'),(227,11,4,'4'),(228,11,4,'5'),(229,11,4,'6'),(230,11,4,'7'),(231,11,4,'8'),(232,11,4,'9'),(233,11,4,'10'),(234,11,4,'11'),(235,11,4,'12'),(236,11,4,'13'),(237,11,4,'14'),(238,11,4,'15'),(239,11,4,'16'),(240,11,4,'17'),(241,11,4,'18'),(242,11,4,'19'),(243,11,4,'20'),(244,11,4,'21'),(245,11,4,'22'),(246,11,4,'23'),(247,11,4,'24'),(248,11,4,'25'),(249,11,4,'26'),(250,11,4,'27'),(251,11,4,'28'),(252,11,4,'29'),(253,11,4,'30'),(254,11,4,'31'),(255,11,4,'32'),(256,11,4,'33'),(257,11,4,'34'),(258,11,4,'35'),(259,11,4,'36'),(260,11,4,'37'),(261,11,4,'38'),(262,11,4,'39'),(263,11,4,'40'),(264,11,4,'41'),(265,11,4,'42'),(266,11,4,'43'),(267,11,4,'44'),(268,11,4,'45'),(269,11,4,'46'),(270,11,4,'47'),(271,11,4,'48'),(272,11,4,'49'),(273,11,4,'50'),(274,11,4,'51'),(275,11,4,'52'),(276,11,4,'53'),(277,11,4,'54'),(278,11,4,'55'),(279,11,4,'56'),(280,11,4,'57'),(281,11,4,'58'),(282,11,4,'59'),(283,11,4,'60'),(284,11,5,'1001'),(285,11,5,'1002'),(286,11,5,'1003'),(287,11,5,'1004'),(288,4,2,'1'),(289,4,2,'2'),(290,4,2,'3'),(291,4,2,'4'),(292,4,2,'5'),(293,4,2,'6'),(294,4,2,'7'),(295,4,2,'8'),(296,4,2,'9'),(297,4,2,'10'),(298,4,2,'11'),(299,4,2,'12'),(300,4,2,'13'),(301,4,2,'14'),(302,4,2,'15'),(303,4,2,'16'),(304,4,2,'17'),(305,4,2,'18'),(306,4,2,'19'),(307,4,2,'20'),(308,4,2,'21'),(309,4,2,'22'),(310,4,2,'23'),(311,4,2,'24'),(312,4,2,'25'),(313,4,2,'26'),(314,4,2,'27'),(315,4,2,'28'),(316,4,2,'29'),(317,4,2,'30'),(318,9,3,'2'),(319,9,3,'4'),(320,9,3,'5'),(321,9,3,'6'),(322,9,3,'7'),(323,9,3,'8'),(324,9,3,'9'),(325,9,3,'10'),(326,9,3,'11'),(327,9,3,'12'),(328,9,3,'13'),(329,9,3,'14'),(330,9,3,'15'),(331,9,3,'16'),(332,9,3,'17'),(333,9,3,'18'),(334,9,3,'19'),(335,9,3,'20'),(336,9,3,'21'),(337,9,3,'22'),(338,9,3,'23'),(339,9,3,'24'),(340,9,3,'25'),(341,9,3,'26'),(342,9,3,'27'),(343,9,3,'28'),(344,9,3,'29'),(345,9,3,'30'),(346,9,3,'31'),(347,9,3,'32'),(348,10,2,'1'),(349,10,2,'1002'),(350,10,2,'1003'),(351,10,2,'1004'),(352,12,6,'1'),(353,12,6,'2'),(354,12,6,'3'),(355,12,6,'4'),(356,12,6,'5'),(357,12,6,'6'),(358,12,6,'7'),(359,12,6,'8'),(360,12,6,'9'),(361,12,6,'10'),(362,12,6,'11'),(363,12,6,'12'),(364,12,6,'13'),(365,12,6,'14'),(366,12,6,'15'),(367,12,6,'16'),(368,12,6,'17'),(369,12,6,'18'),(370,12,6,'19'),(371,12,6,'20'),(372,12,6,'21'),(373,12,6,'22'),(374,12,6,'23'),(375,12,6,'24'),(376,12,6,'25'),(377,12,6,'26'),(378,12,6,'27'),(379,12,6,'28'),(380,12,6,'29'),(381,12,6,'30'),(382,12,6,'31'),(383,12,6,'32'),(384,12,6,'33'),(385,12,6,'34'),(386,12,6,'35'),(387,12,6,'36'),(388,12,6,'37'),(389,12,6,'38'),(390,12,6,'39'),(391,12,6,'40'),(392,12,6,'41'),(393,12,6,'42'),(394,12,6,'43'),(395,12,6,'44'),(396,12,6,'45'),(397,12,6,'46'),(398,12,6,'47'),(399,12,6,'48'),(400,12,6,'49'),(401,12,6,'50'),(402,12,6,'51'),(403,12,6,'52'),(404,12,6,'53'),(405,12,6,'54'),(406,12,6,'55'),(407,12,6,'56'),(408,12,6,'57'),(409,12,6,'58'),(410,12,6,'59'),(411,12,6,'60'),(412,12,6,'61'),(413,12,6,'62'),(414,12,6,'63'),(415,12,6,'64'),(416,12,6,'65'),(417,12,6,'66'),(418,12,6,'67'),(419,12,6,'68'),(420,12,6,'69'),(421,12,6,'70'),(422,12,6,'71'),(423,12,6,'72'),(424,12,6,'73'),(425,12,6,'74'),(426,12,6,'75'),(427,12,6,'76'),(428,12,6,'77'),(429,12,6,'78'),(430,12,6,'79'),(431,12,6,'80'),(432,12,6,'81'),(433,12,6,'82'),(434,12,6,'83'),(435,12,6,'84'),(436,12,6,'85'),(437,12,6,'86'),(438,12,6,'87'),(439,12,6,'88'),(440,12,6,'89'),(441,12,6,'90'),(442,12,6,'91'),(443,12,6,'92'),(444,12,6,'93'),(445,12,6,'94'),(446,12,6,'95'),(447,12,6,'96'),(448,12,6,'97'),(449,12,6,'98'),(450,12,6,'99'),(451,12,6,'100'),(452,12,6,'101'),(453,12,6,'102'),(454,12,6,'103'),(455,12,6,'104'),(456,12,6,'105'),(457,12,6,'106'),(458,12,6,'107'),(459,12,6,'108'),(460,12,6,'109'),(461,12,6,'110'),(462,12,6,'111'),(463,12,6,'112'),(464,12,6,'113'),(465,12,6,'114'),(466,12,6,'115'),(467,12,6,'116'),(468,12,6,'117'),(469,12,6,'118'),(470,12,6,'119'),(471,12,6,'120'),(472,12,6,'121'),(473,12,6,'122'),(474,12,6,'123'),(475,12,6,'124'),(476,12,6,'125'),(477,12,6,'126'),(478,12,6,'127'),(479,12,6,'128'),(480,12,6,'129'),(481,12,6,'130'),(482,12,6,'131'),(483,12,6,'132'),(484,12,6,'133'),(485,12,6,'134'),(486,12,6,'135'),(487,12,6,'136'),(488,12,6,'137'),(489,12,6,'138'),(490,12,6,'139'),(491,12,6,'140'),(492,12,6,'141'),(493,12,6,'142'),(494,12,6,'143'),(495,12,6,'144'),(496,12,6,'145'),(497,12,6,'146'),(498,12,6,'147'),(499,12,6,'148'),(500,12,6,'149'),(501,12,6,'150'),(502,12,6,'151'),(503,12,6,'152'),(504,12,6,'153'),(505,12,6,'154'),(506,12,6,'155'),(507,12,6,'156'),(508,12,6,'157'),(509,12,6,'158'),(510,12,6,'159'),(511,12,6,'160'),(512,12,6,'161'),(513,12,6,'162'),(514,12,6,'163'),(515,12,6,'164'),(516,12,6,'165'),(517,12,6,'166'),(518,12,6,'167'),(519,12,6,'168'),(520,12,6,'169'),(521,13,5,'9'),(522,13,5,'10'),(523,13,5,'11'),(524,13,5,'12'),(525,13,5,'13'),(526,13,5,'14'),(527,13,5,'15'),(528,13,5,'16'),(529,13,5,'17'),(530,13,5,'18'),(531,13,5,'19'),(532,13,5,'20'),(533,13,5,'21'),(534,13,5,'22'),(535,13,5,'23'),(536,13,5,'24'),(537,13,5,'25'),(538,13,5,'26'),(539,13,5,'27'),(540,13,5,'28'),(541,13,5,'29'),(542,13,5,'30'),(543,13,5,'31'),(544,13,5,'32'),(545,13,5,'33'),(546,13,5,'34'),(547,13,5,'35'),(548,13,5,'36'),(549,13,5,'37'),(550,13,5,'38'),(551,13,5,'39'),(552,13,5,'40'),(553,13,5,'41'),(554,13,5,'42'),(555,13,5,'43'),(556,13,5,'44'),(557,13,5,'45'),(558,13,5,'46'),(559,13,5,'47'),(560,13,5,'48'),(561,13,5,'49'),(562,13,5,'50'),(563,13,5,'51'),(564,13,5,'52'),(565,13,5,'53'),(566,13,5,'54'),(567,13,5,'55'),(568,13,5,'56'),(569,13,5,'57'),(570,13,5,'58'),(571,13,5,'59'),(572,13,5,'60'),(573,13,5,'61'),(574,13,5,'62'),(575,13,5,'63'),(576,13,5,'64'),(577,13,5,'65'),(578,13,5,'66'),(579,13,5,'67'),(580,13,5,'68'),(581,13,5,'69'),(582,13,5,'70'),(583,13,5,'71'),(584,13,5,'72'),(585,13,5,'73'),(586,13,5,'74'),(587,13,5,'75'),(588,13,5,'76'),(589,13,5,'77'),(590,13,5,'78'),(591,13,5,'79'),(592,13,5,'80'),(593,13,5,'81'),(594,13,5,'82'),(595,13,5,'83'),(596,14,4,'1'),(597,14,4,'2'),(598,14,4,'3'),(599,14,4,'4'),(600,14,4,'5'),(601,14,4,'6'),(602,14,4,'7'),(603,14,4,'8'),(604,14,4,'9'),(605,14,4,'10'),(606,14,4,'11'),(607,14,4,'12'),(608,14,4,'13'),(609,14,4,'14'),(610,14,4,'15'),(611,14,4,'16'),(612,14,4,'17'),(613,14,4,'18'),(614,14,4,'19'),(615,14,4,'20'),(616,14,4,'21'),(617,14,4,'22'),(618,14,4,'23'),(619,14,4,'24'),(620,14,4,'25'),(621,14,4,'26'),(622,14,4,'27'),(623,14,4,'28'),(624,14,4,'29'),(625,14,4,'30'),(626,14,5,'1001'),(627,14,5,'1002'),(628,14,5,'1003'),(629,14,5,'1004'),(630,14,5,'1005'),(631,14,5,'1006'),(632,27,7,'44'),(633,27,7,'43'),(634,27,7,'45'),(635,27,7,'53'),(636,27,7,'55'),(637,27,7,'60'),(638,27,7,'62'),(639,27,7,'50'),(640,27,7,'51'),(641,27,7,'59'),(642,27,7,'46'),(643,27,7,'48'),(644,27,7,'49'),(645,27,7,'4'),(646,27,7,'5'),(647,27,7,'47'),(648,27,7,'58'),(649,27,7,'57'),(650,27,7,'56'),(651,28,7,'1'),(652,28,7,'2'),(653,28,7,'3'),(654,28,7,'4'),(655,28,7,'5'),(656,28,7,'6'),(657,28,7,'7'),(658,28,7,'8'),(659,28,7,'9'),(660,29,8,'3'),(661,29,8,'2'),(662,29,8,'1'),(663,29,8,'4'),(664,30,8,'2'),(665,30,8,'1'),(666,31,8,'1'),(667,31,8,'2'),(668,31,8,'6'),(669,31,8,'5'),(670,31,8,'4'),(671,31,8,'9'),(672,31,8,'13'),(673,31,8,'8'),(674,31,8,'10'),(675,31,8,'11'),(676,31,8,'12'),(677,31,8,'14'),(678,31,8,'15'),(679,31,8,'7'),(680,31,8,'3'),(681,32,2,'24'),(682,32,2,'4'),(683,32,2,'5'),(684,32,2,'6'),(685,32,2,'25'),(686,32,2,'11'),(687,32,2,'12'),(688,32,2,'22'),(689,32,2,'2'),(690,32,2,'16'),(691,32,2,'10'),(692,32,2,'18'),(693,32,2,'15'),(694,32,2,'23'),(695,32,2,'33'),(696,32,2,'28'),(697,33,2,'32'),(698,33,2,'26'),(699,33,2,'17'),(700,33,2,'8'),(701,33,2,'29'),(702,33,2,'34'),(703,33,2,'3'),(704,33,2,'21'),(705,33,2,'31'),(706,33,2,'7'),(707,33,2,'14'),(708,33,2,'13'),(709,33,2,'19'),(710,33,2,'9'),(711,33,2,'30'),(712,33,2,'20'),(713,34,2,'26'),(714,34,2,'6'),(715,34,2,'9'),(716,34,2,'12'),(717,34,2,'25'),(718,34,2,'8'),(719,34,2,'13'),(720,34,2,'16'),(721,34,2,'18'),(722,34,2,'7'),(723,34,2,'24'),(724,34,2,'10'),(725,34,2,'4'),(726,34,2,'2'),(727,34,2,'29'),(728,34,2,'15'),(729,34,2,'14'),(730,34,2,'20'),(731,34,2,'21'),(732,34,2,'11'),(733,34,2,'3'),(734,34,2,'22'),(735,34,2,'5'),(736,34,2,'19'),(737,34,2,'17'),(738,34,2,'27'),(739,34,2,'30'),(740,34,2,'23'),(741,35,2,'1'),(742,35,2,'2'),(743,35,2,'3'),(744,35,2,'4'),(745,35,2,'5'),(746,35,2,'6'),(747,35,2,'7'),(748,35,2,'8'),(749,36,2,'1'),(750,36,2,'2'),(751,36,2,'3'),(752,36,2,'4'),(753,36,2,'5'),(754,36,2,'6'),(755,36,2,'7'),(756,36,2,'8'),(757,37,2,'1'),(758,37,2,'2'),(759,37,2,'3'),(760,37,2,'4'),(761,37,2,'5'),(762,37,2,'6'),(763,37,2,'7'),(764,37,2,'8'),(765,38,2,'1'),(766,38,2,'2'),(767,38,2,'3'),(768,38,2,'4'),(769,38,2,'5'),(770,38,2,'6'),(771,38,2,'7'),(772,38,2,'8'),(773,39,2,'1'),(774,39,2,'2'),(775,39,2,'3'),(776,39,2,'4'),(777,39,2,'5'),(778,39,2,'6'),(779,39,2,'7'),(780,39,2,'8'),(781,40,8,'2'),(782,40,8,'1'),(783,40,8,'3'),(784,40,8,'4'),(785,41,8,'1'),(786,41,8,'2'),(787,41,8,'3'),(788,41,8,'4'),(789,41,8,'5'),(790,41,8,'6'),(791,41,8,'7'),(792,41,8,'10'),(793,41,8,'11'),(794,41,8,'12'),(795,41,8,'13'),(796,41,8,'14'),(797,41,8,'15'),(798,41,8,'16'),(799,41,8,'8'),(800,41,8,'9');
/*!40000 ALTER TABLE `inventory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventory__document`
--

DROP TABLE IF EXISTS `inventory__document`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `inventory__document` (
  `inventory__document_id` int(11) NOT NULL AUTO_INCREMENT,
  `inventory_id` int(11) DEFAULT NULL,
  `document_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`inventory__document_id`),
  KEY `Ref_240` (`document_id`),
  KEY `Ref_241` (`inventory_id`),
  CONSTRAINT `Ref_240` FOREIGN KEY (`document_id`) REFERENCES `document` (`document_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Ref_241` FOREIGN KEY (`inventory_id`) REFERENCES `inventory` (`inventory_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory__document`
--

LOCK TABLES `inventory__document` WRITE;
/*!40000 ALTER TABLE `inventory__document` DISABLE KEYS */;
/*!40000 ALTER TABLE `inventory__document` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventory__elogentry`
--

DROP TABLE IF EXISTS `inventory__elogentry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `inventory__elogentry` (
  `inventory__elogentry_id` int(11) NOT NULL AUTO_INCREMENT,
  `inventory_id` int(11) NOT NULL DEFAULT '0',
  `elog_entry_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`inventory__elogentry_id`),
  KEY `Ref_144` (`inventory_id`),
  KEY `Ref_145` (`elog_entry_id`),
  CONSTRAINT `Ref_144` FOREIGN KEY (`inventory_id`) REFERENCES `inventory` (`inventory_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Ref_145` FOREIGN KEY (`elog_entry_id`) REFERENCES `elog_entry` (`elog_entry_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory__elogentry`
--

LOCK TABLES `inventory__elogentry` WRITE;
/*!40000 ALTER TABLE `inventory__elogentry` DISABLE KEYS */;
/*!40000 ALTER TABLE `inventory__elogentry` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventory__install`
--

DROP TABLE IF EXISTS `inventory__install`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `inventory__install` (
  `inventory__install_id` int(11) NOT NULL AUTO_INCREMENT,
  `install_id` int(11) NOT NULL DEFAULT '0',
  `inventory_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`inventory__install_id`),
  KEY `Ref_104` (`install_id`),
  KEY `Ref_102` (`inventory_id`),
  CONSTRAINT `Ref_104` FOREIGN KEY (`install_id`) REFERENCES `install` (`install_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Ref_102` FOREIGN KEY (`inventory_id`) REFERENCES `inventory` (`inventory_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=740 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory__install`
--

LOCK TABLES `inventory__install` WRITE;
/*!40000 ALTER TABLE `inventory__install` DISABLE KEYS */;
INSERT INTO `inventory__install` VALUES (1,3,430),(2,4,164),(3,6,91),(4,7,434),(5,8,165),(6,9,436),(7,13,310),(8,14,582),(9,16,275),(10,17,623),(11,18,276),(12,19,498),(13,20,63),(14,23,326),(15,24,561),(16,26,117),(17,27,364),(18,29,150),(19,30,365),(20,33,425),(21,34,146),(22,36,432),(23,37,78),(24,39,435),(25,40,147),(26,43,315),(27,44,484),(28,46,242),(29,47,624),(30,48,265),(31,49,485),(32,50,56),(33,54,542),(34,55,327),(35,56,557),(36,57,116),(37,59,152),(38,60,369),(39,63,418),(40,64,158),(41,66,77),(42,67,419),(43,68,155),(44,69,420),(45,73,291),(46,74,521),(47,76,227),(48,77,599),(49,78,229),(50,79,377),(51,80,49),(52,83,330),(53,84,548),(54,86,114),(55,87,389),(56,89,153),(57,90,415),(58,93,447),(59,94,167),(60,96,446),(61,97,92),(62,99,445),(63,100,170),(64,103,292),(65,104,527),(66,106,237),(67,107,602),(68,108,238),(69,109,378),(70,110,45),(71,114,575),(72,115,333),(73,116,576),(74,117,120),(75,119,175),(76,120,487),(77,123,486),(78,124,184),(79,126,99),(80,127,488),(81,128,185),(82,129,489),(83,133,296),(84,134,537),(85,136,243),(86,137,603),(87,138,241),(88,139,381),(89,140,50),(90,143,328),(91,144,564),(92,146,109),(93,147,437),(94,149,157),(95,150,438),(96,153,426),(97,154,186),(98,156,427),(99,157,97),(100,159,455),(101,160,187),(102,163,295),(103,164,526),(104,166,239),(105,167,604),(106,168,240),(107,169,380),(108,170,48),(109,174,571),(110,175,331),(111,176,572),(112,177,118),(113,179,163),(114,180,451),(115,183,397),(116,184,148),(117,186,76),(118,187,408),(119,188,149),(120,189,409),(121,193,298),(122,194,530),(123,196,251),(124,197,605),(125,198,252),(126,199,382),(127,200,51),(128,203,323),(129,204,541),(130,206,108),(131,207,411),(132,209,140),(133,210,362),(134,213,449),(135,214,178),(136,216,450),(137,217,96),(138,219,454),(139,220,180),(140,223,306),(141,224,563),(142,226,266),(143,227,609),(144,228,267),(145,229,416),(146,230,61),(147,234,570),(148,235,350),(149,236,574),(150,237,121),(151,239,172),(152,240,443),(153,243,367),(154,244,171),(155,246,93),(156,247,441),(157,248,222),(158,249,448),(159,253,297),(160,254,562),(161,256,244),(162,257,614),(163,258,261),(164,259,417),(165,260,47),(166,263,332),(167,264,568),(168,266,119),(169,267,428),(170,269,168),(171,270,429),(172,273,414),(173,274,154),(174,276,394),(175,277,71),(176,279,395),(177,280,151),(178,283,294),(179,284,525),(180,286,231),(181,287,606),(182,288,234),(183,289,383),(184,290,54),(185,294,552),(186,295,325),(187,296,554),(188,297,107),(189,299,141),(190,300,399),(191,303,493),(192,304,176),(193,306,90),(194,307,494),(195,308,177),(196,309,495),(197,313,307),(198,314,539),(199,316,259),(200,317,608),(201,318,245),(202,319,407),(203,320,52),(204,323,324),(205,324,560),(206,326,110),(207,327,392),(208,329,142),(209,330,393),(210,333,461),(211,334,183),(212,336,462),(213,337,79),(214,339,463),(215,340,200),(216,343,299),(217,344,546),(218,346,253),(219,347,612),(220,348,254),(221,349,396),(222,350,55),(223,354,573),(224,355,338),(225,356,569),(226,357,123),(227,359,181),(228,360,471),(229,363,475),(230,364,188),(231,366,98),(232,367,459),(233,368,191),(234,369,460),(235,373,303),(236,374,543),(237,376,228),(238,377,610),(239,378,246),(240,379,357),(241,380,64),(242,383,334),(243,384,549),(244,386,122),(245,387,431),(246,389,179),(247,390,433),(248,393,465),(249,394,190),(250,396,466),(251,397,81),(252,399,497),(253,400,194),(254,403,308),(255,404,550),(256,406,247),(257,407,607),(258,408,248),(259,409,368),(260,410,62),(261,414,583),(262,415,335),(263,416,584),(264,417,126),(265,419,192),(266,420,505),(267,423,477),(268,424,196),(269,426,84),(270,427,479),(271,428,197),(272,429,482),(273,433,304),(274,434,544),(275,436,255),(276,437,615),(277,438,256),(278,439,398),(279,440,53),(280,443,336),(281,444,585),(282,446,124),(283,447,503),(284,449,189),(285,450,504),(286,453,440),(287,454,195),(288,456,500),(289,457,87),(290,459,502),(291,460,198),(292,463,301),(293,464,559),(294,466,257),(295,467,611),(296,468,258),(297,469,370),(298,470,46),(299,474,580),(300,475,337),(301,476,581),(302,477,125),(303,479,199),(304,480,483),(305,483,464),(306,484,203),(307,486,88),(308,487,473),(309,488,204),(310,489,511),(311,493,309),(312,494,547),(313,496,262),(314,497,613),(315,498,263),(316,499,400),(317,500,57),(318,503,341),(319,504,593),(320,506,127),(321,507,506),(322,509,201),(323,510,507),(324,513,469),(325,514,208),(326,516,472),(327,517,82),(328,519,513),(329,520,193),(330,523,314),(331,524,588),(332,526,277),(333,527,628),(334,528,278),(335,529,468),(336,530,69),(337,534,590),(338,535,349),(339,536,591),(340,537,101),(341,539,202),(342,540,510),(343,543,480),(344,544,206),(345,546,83),(346,547,512),(347,548,223),(348,549,515),(349,553,312),(350,554,586),(351,556,273),(352,557,630),(353,558,274),(354,559,496),(355,560,59),(356,563,340),(357,564,595),(358,566,130),(359,567,467),(360,569,210),(361,570,478),(362,573,352),(363,574,169),(364,576,356),(365,577,94),(366,579,514),(367,580,220),(368,583,317),(369,584,567),(370,586,279),(371,587,631),(372,588,280),(373,589,499),(374,590,67),(375,594,553),(376,595,347),(377,596,594),(378,597,115),(379,599,219),(380,600,509),(381,603,518),(382,604,205),(383,606,89),(384,607,519),(385,608,212),(386,609,520),(387,613,316),(388,614,578),(389,616,270),(390,617,626),(391,618,283),(392,619,442),(393,620,65),(394,623,339),(395,624,529),(396,626,129),(397,627,481),(398,629,214),(399,630,517),(400,633,424),(401,634,216),(402,636,470),(403,637,85),(404,639,476),(405,640,182),(406,643,313),(407,644,587),(408,646,281),(409,647,627),(410,648,282),(411,649,474),(412,650,70),(413,654,538),(414,655,343),(415,656,592),(416,657,128),(417,659,211),(418,660,444),(419,663,366),(420,664,209),(421,666,100),(422,667,439),(423,668,213),(424,669,501),(425,673,300),(426,674,577),(427,676,271),(428,677,629),(429,678,272),(430,679,457),(431,680,68),(432,683,344),(433,684,589),(434,686,112),(435,687,508),(436,689,207),(437,690,516),(438,693,453),(439,694,161),(440,696,456),(441,697,86),(442,699,458),(443,700,166),(444,703,302),(445,704,558),(446,706,249),(447,707,616),(448,708,250),(449,709,404),(450,710,58),(451,714,565),(452,715,329),(453,716,566),(454,717,111),(455,719,160),(456,720,452),(457,723,490),(458,724,173),(459,726,95),(460,727,491),(461,728,174),(462,729,492),(463,733,288),(464,734,522),(465,736,224),(466,737,596),(467,738,225),(468,739,361),(469,740,41),(470,743,319),(471,744,523),(472,746,102),(473,747,372),(474,749,131),(475,750,373),(476,753,363),(477,754,132),(478,756,371),(479,757,72),(480,759,376),(481,760,133),(482,763,289),(483,764,524),(484,766,226),(485,767,597),(486,768,235),(487,769,374),(488,770,42),(489,774,535),(490,775,318),(491,776,531),(492,777,104),(493,779,136),(494,780,401),(495,783,384),(496,784,138),(497,786,74),(498,787,385),(499,788,139),(500,789,386),(501,793,290),(502,794,534),(503,796,233),(504,797,598),(505,798,236),(506,799,375),(507,800,43),(508,803,320),(509,804,533),(510,806,103),(511,807,402),(512,809,134),(513,810,403),(514,813,359),(515,814,156),(516,816,360),(517,817,73),(518,819,410),(519,820,159),(520,823,311),(521,824,540),(522,826,260),(523,827,618),(524,828,264),(525,829,412),(526,830,60),(527,834,555),(528,835,348),(529,836,556),(530,837,113),(531,839,145),(532,840,358),(533,843,421),(534,844,162),(535,846,80),(536,847,422),(537,848,221),(538,849,423),(539,853,305),(540,854,551),(541,856,268),(542,857,619),(543,858,269),(544,859,413),(545,860,66),(546,863,321),(547,864,528),(548,866,105),(549,867,405),(550,869,137),(551,870,406),(552,873,388),(553,874,143),(554,876,390),(555,877,75),(556,879,391),(557,880,144),(558,883,293),(559,884,536),(560,886,230),(561,887,600),(562,888,232),(563,889,379),(564,890,44),(565,894,545),(566,895,322),(567,896,532),(568,897,106),(569,899,135),(570,900,387),(571,901,632),(572,902,633),(573,903,634),(574,904,635),(575,905,636),(576,906,637),(577,907,638),(578,908,639),(579,909,640),(580,910,641),(581,911,642),(582,912,643),(583,913,644),(584,914,645),(585,915,646),(586,916,647),(587,917,648),(588,918,649),(589,919,650),(590,920,651),(591,921,652),(592,922,653),(593,923,654),(594,924,655),(595,925,656),(596,926,657),(597,927,658),(598,928,659),(599,929,660),(600,930,661),(601,931,662),(602,932,663),(603,933,664),(604,934,665),(605,935,666),(606,936,667),(607,937,668),(608,938,669),(609,939,670),(610,940,671),(611,941,672),(612,942,673),(613,943,674),(614,944,675),(615,945,676),(616,946,677),(617,947,678),(618,948,679),(619,949,680),(620,950,681),(621,951,682),(622,952,683),(623,953,684),(624,954,685),(625,955,686),(626,956,687),(627,957,688),(628,958,689),(629,959,690),(630,960,691),(631,961,692),(632,962,693),(633,963,694),(634,964,695),(635,965,696),(636,966,697),(637,967,698),(638,968,699),(639,969,700),(640,970,701),(641,971,702),(642,972,703),(643,973,704),(644,974,705),(645,975,706),(646,976,707),(647,977,708),(648,978,709),(649,979,710),(650,980,711),(651,981,712),(652,982,713),(653,983,714),(654,984,715),(655,985,716),(656,986,717),(657,987,718),(658,988,719),(659,989,720),(660,990,721),(661,991,722),(662,992,723),(663,993,724),(664,994,725),(665,995,726),(666,996,727),(667,997,728),(668,998,729),(669,999,730),(670,1000,731),(671,1001,732),(672,1002,733),(673,1003,734),(674,1004,735),(675,1005,736),(676,1006,737),(677,1007,738),(678,1008,739),(679,1009,740),(680,1010,741),(681,1011,742),(682,1012,743),(683,1013,744),(684,1014,745),(685,1015,746),(686,1016,747),(687,1017,748),(688,1018,749),(689,1019,750),(690,1020,751),(691,1021,752),(692,1022,753),(693,1023,754),(694,1024,755),(695,1025,756),(696,1026,757),(697,1027,758),(698,1028,759),(699,1029,760),(700,1030,761),(701,1031,762),(702,1032,763),(703,1033,764),(704,1034,765),(705,1035,766),(706,1036,767),(707,1037,768),(708,1038,769),(709,1039,770),(710,1040,771),(711,1041,772),(712,1042,773),(713,1043,774),(714,1044,775),(715,1045,776),(716,1046,777),(717,1047,778),(718,1048,779),(719,1049,780),(720,1050,781),(721,1051,782),(722,1052,783),(723,1053,784),(724,1054,785),(725,1055,786),(726,1056,787),(727,1057,788),(728,1058,789),(729,1059,790),(730,1060,791),(731,1061,792),(732,1062,793),(733,1063,794),(734,1064,795),(735,1065,796),(736,1066,797),(737,1067,798),(738,1068,799),(739,1069,800);
/*!40000 ALTER TABLE `inventory__install` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventory_prop`
--

DROP TABLE IF EXISTS `inventory_prop`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `inventory_prop` (
  `inventory_prop_id` int(11) NOT NULL AUTO_INCREMENT,
  `inventory_id` int(11) NOT NULL,
  `inventory_prop_tmplt_id` int(11) NOT NULL DEFAULT '0',
  `inventory_prop_value` varchar(4096) DEFAULT NULL,
  PRIMARY KEY (`inventory_prop_id`),
  KEY `idx_cmpnt_id` (`inventory_id`),
  KEY `Ref_172` (`inventory_prop_tmplt_id`),
  CONSTRAINT `Ref_71` FOREIGN KEY (`inventory_id`) REFERENCES `inventory` (`inventory_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Ref_172` FOREIGN KEY (`inventory_prop_tmplt_id`) REFERENCES `inventory_prop_tmplt` (`inventory_prop_tmplt_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=709 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory_prop`
--

LOCK TABLES `inventory_prop` WRITE;
/*!40000 ALTER TABLE `inventory_prop` DISABLE KEYS */;
/*!40000 ALTER TABLE `inventory_prop` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventory_prop_tmplt`
--

DROP TABLE IF EXISTS `inventory_prop_tmplt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `inventory_prop_tmplt` (
  `inventory_prop_tmplt_id` int(11) NOT NULL AUTO_INCREMENT,
  `cmpnt_type_id` int(11) NOT NULL DEFAULT '0',
  `inventory_prop_tmplt_name` varchar(50) DEFAULT NULL,
  `inventory_prop_tmplt_desc` varchar(255) DEFAULT NULL,
  `inventory_prop_tmplt_default` varchar(255) DEFAULT NULL,
  `inventory_prop_tmplt_units` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`inventory_prop_tmplt_id`),
  KEY `Ref_169` (`cmpnt_type_id`),
  CONSTRAINT `Ref_169` FOREIGN KEY (`cmpnt_type_id`) REFERENCES `cmpnt_type` (`cmpnt_type_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory_prop_tmplt`
--

LOCK TABLES `inventory_prop_tmplt` WRITE;
/*!40000 ALTER TABLE `inventory_prop_tmplt` DISABLE KEYS */;
INSERT INTO `inventory_prop_tmplt` VALUES (1,16,'municonv','unit conversion parameters for NSLS II magnets',NULL,NULL),(2,17,'municonv','unit conversion parameters for NSLS II magnets',NULL,NULL),(3,15,'municonv','unit conversion parameters for NSLS II magnets',NULL,NULL),(4,3,'municonv','unit conversion parameters for NSLS II magnets',NULL,NULL),(5,5,'municonv','unit conversion parameters for NSLS II magnets',NULL,NULL),(6,6,'municonv','unit conversion parameters for NSLS II magnets',NULL,NULL),(7,7,'municonv','unit conversion parameters for NSLS II magnets',NULL,NULL),(8,8,'municonv','unit conversion parameters for NSLS II magnets',NULL,NULL),(9,11,'municonv','unit conversion parameters for NSLS II magnets',NULL,NULL),(10,4,'municonv','unit conversion parameters for NSLS II magnets',NULL,NULL),(11,9,'municonv','unit conversion parameters for NSLS II magnets',NULL,NULL),(12,10,'municonv','unit conversion parameters for NSLS II magnets',NULL,NULL),(13,12,'municonv','unit conversion parameters for NSLS II magnets',NULL,NULL),(14,13,'municonv','unit conversion parameters for NSLS II magnets',NULL,NULL),(15,14,'municonv','unit conversion parameters for NSLS II magnets',NULL,NULL),(16,27,'municonv','unit conversion parameters for NSLS II magnets',NULL,NULL),(17,27,'municonv_chain','unit conversion parameters for NSLS II magnets, which is a chain powered by a common power supply.',NULL,NULL),(18,28,'municonv','unit conversion parameters for NSLS II magnets',NULL,NULL),(19,31,'municonv','unit conversion parameters for NSLS II magnets',NULL,NULL),(20,41,'municonv','unit conversion parameters for NSLS II magnets',NULL,NULL);
/*!40000 ALTER TABLE `inventory_prop_tmplt` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ioc`
--

DROP TABLE IF EXISTS `ioc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ioc` (
  `ioc_id` int(11) NOT NULL AUTO_INCREMENT,
  `ioc_status_id` int(11) DEFAULT NULL,
  `ioc_nm` varchar(255) DEFAULT NULL,
  `system` varchar(255) DEFAULT NULL,
  `ioc_boot_instructions` text,
  `modified_by` varchar(50) DEFAULT NULL,
  `modified_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ioc_id`),
  UNIQUE KEY `ioc_nm` (`ioc_nm`),
  KEY `Ref_202` (`ioc_status_id`),
  CONSTRAINT `Ref_202` FOREIGN KEY (`ioc_status_id`) REFERENCES `ioc_status` (`ioc_status_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ioc`
--

LOCK TABLES `ioc` WRITE;
/*!40000 ALTER TABLE `ioc` DISABLE KEYS */;
/*!40000 ALTER TABLE `ioc` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ioc_boot`
--

DROP TABLE IF EXISTS `ioc_boot`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ioc_boot` (
  `ioc_boot_id` int(11) NOT NULL AUTO_INCREMENT,
  `ioc_id` int(11) DEFAULT NULL,
  `sys_boot_line` varchar(127) DEFAULT NULL,
  `ioc_boot_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `current_load` tinyint(1) DEFAULT NULL,
  `current_boot` tinyint(1) DEFAULT NULL,
  `modified_date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `modified_by` varchar(10) DEFAULT NULL,
  `boot_device` varchar(50) DEFAULT NULL,
  `boot_params_version` float DEFAULT NULL,
  `console_connection` varchar(127) DEFAULT NULL,
  `host_inet_address` varchar(127) DEFAULT NULL,
  `host_name` varchar(127) DEFAULT NULL,
  `ioc_inet_address` varchar(127) DEFAULT NULL,
  `ioc_pid` int(11) DEFAULT NULL,
  `launch_script` varchar(127) DEFAULT NULL,
  `launch_script_pid` int(11) DEFAULT NULL,
  `os_file_name` varchar(127) DEFAULT NULL,
  `processor_number` int(11) DEFAULT NULL,
  `target_architecture` varchar(127) DEFAULT NULL,
  `ioc_status` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ioc_boot_id`),
  KEY `idx_current_load` (`current_load`),
  KEY `idx_ioc_id` (`ioc_id`),
  CONSTRAINT `Ref_54` FOREIGN KEY (`ioc_id`) REFERENCES `ioc` (`ioc_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ioc_boot`
--

LOCK TABLES `ioc_boot` WRITE;
/*!40000 ALTER TABLE `ioc_boot` DISABLE KEYS */;
/*!40000 ALTER TABLE `ioc_boot` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ioc_error`
--

DROP TABLE IF EXISTS `ioc_error`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ioc_error` (
  `ioc_error_id` int(11) NOT NULL AUTO_INCREMENT,
  `ioc_boot_id` int(11) DEFAULT NULL,
  `ioc_error_message_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`ioc_error_id`),
  KEY `idx_ioc_boot_id` (`ioc_boot_id`),
  KEY `idx_ioc_error_num` (`ioc_error_message_id`),
  CONSTRAINT `ioc_error_ibfk_1` FOREIGN KEY (`ioc_boot_id`) REFERENCES `ioc_boot` (`ioc_boot_id`),
  CONSTRAINT `Ref_77` FOREIGN KEY (`ioc_error_message_id`) REFERENCES `ioc_error_message` (`ioc_error_message_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ioc_error`
--

LOCK TABLES `ioc_error` WRITE;
/*!40000 ALTER TABLE `ioc_error` DISABLE KEYS */;
/*!40000 ALTER TABLE `ioc_error` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ioc_error_message`
--

DROP TABLE IF EXISTS `ioc_error_message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ioc_error_message` (
  `ioc_error_message_id` int(11) NOT NULL AUTO_INCREMENT,
  `ioc_error_message` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`ioc_error_message_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ioc_error_message`
--

LOCK TABLES `ioc_error_message` WRITE;
/*!40000 ALTER TABLE `ioc_error_message` DISABLE KEYS */;
/*!40000 ALTER TABLE `ioc_error_message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ioc_prop`
--

DROP TABLE IF EXISTS `ioc_prop`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ioc_prop` (
  `ioc_prop_id` int(11) NOT NULL AUTO_INCREMENT,
  `ioc_id` int(11) DEFAULT NULL,
  `ioc_proptype_id` int(11) NOT NULL DEFAULT '0',
  `ioc_prop_value` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ioc_prop_id`),
  KEY `Ref_222` (`ioc_id`),
  KEY `Ref_223` (`ioc_proptype_id`),
  CONSTRAINT `Ref_222` FOREIGN KEY (`ioc_id`) REFERENCES `ioc` (`ioc_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Ref_223` FOREIGN KEY (`ioc_proptype_id`) REFERENCES `ioc_proptype` (`ioc_proptype_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ioc_prop`
--

LOCK TABLES `ioc_prop` WRITE;
/*!40000 ALTER TABLE `ioc_prop` DISABLE KEYS */;
/*!40000 ALTER TABLE `ioc_prop` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ioc_proptype`
--

DROP TABLE IF EXISTS `ioc_proptype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ioc_proptype` (
  `ioc_proptype_id` int(11) NOT NULL AUTO_INCREMENT,
  `ioc_proptype_name` varchar(50) DEFAULT NULL,
  `ioc_proptype_desc` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ioc_proptype_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ioc_proptype`
--

LOCK TABLES `ioc_proptype` WRITE;
/*!40000 ALTER TABLE `ioc_proptype` DISABLE KEYS */;
/*!40000 ALTER TABLE `ioc_proptype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ioc_resource`
--

DROP TABLE IF EXISTS `ioc_resource`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ioc_resource` (
  `ioc_resource_id` int(11) NOT NULL AUTO_INCREMENT,
  `ioc_boot_id` int(11) DEFAULT NULL,
  `text_line` varchar(255) DEFAULT NULL,
  `load_order` int(11) DEFAULT NULL,
  `uri_id` int(11) DEFAULT NULL,
  `unreachable` tinyint(1) DEFAULT NULL,
  `subst_str` varchar(255) DEFAULT NULL,
  `ioc_resource_type_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`ioc_resource_id`),
  KEY `idx_ioc_boot_id` (`ioc_boot_id`),
  KEY `idx_uri_id` (`uri_id`),
  KEY `idx_ioc_resource_type_id` (`ioc_resource_type_id`),
  CONSTRAINT `ioc_resource_ibfk_1` FOREIGN KEY (`ioc_boot_id`) REFERENCES `ioc_boot` (`ioc_boot_id`),
  CONSTRAINT `ioc_resource_ibfk_2` FOREIGN KEY (`uri_id`) REFERENCES `uri` (`uri_id`),
  CONSTRAINT `Ref_78` FOREIGN KEY (`ioc_resource_type_id`) REFERENCES `ioc_resource_type` (`ioc_resource_type_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ioc_resource`
--

LOCK TABLES `ioc_resource` WRITE;
/*!40000 ALTER TABLE `ioc_resource` DISABLE KEYS */;
/*!40000 ALTER TABLE `ioc_resource` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ioc_resource_type`
--

DROP TABLE IF EXISTS `ioc_resource_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ioc_resource_type` (
  `ioc_resource_type_id` int(11) NOT NULL,
  `ioc_resource_type` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`ioc_resource_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ioc_resource_type`
--

LOCK TABLES `ioc_resource_type` WRITE;
/*!40000 ALTER TABLE `ioc_resource_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `ioc_resource_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ioc_status`
--

DROP TABLE IF EXISTS `ioc_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ioc_status` (
  `ioc_status_id` int(11) NOT NULL AUTO_INCREMENT,
  `ioc_status` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ioc_status_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ioc_status`
--

LOCK TABLES `ioc_status` WRITE;
/*!40000 ALTER TABLE `ioc_status` DISABLE KEYS */;
/*!40000 ALTER TABLE `ioc_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `iocboot__install`
--

DROP TABLE IF EXISTS `iocboot__install`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `iocboot__install` (
  `iocboot__install_id` int(11) NOT NULL AUTO_INCREMENT,
  `install_id` int(11) DEFAULT NULL,
  `ioc_boot_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`iocboot__install_id`),
  KEY `Ref_125` (`install_id`),
  KEY `Ref_203` (`ioc_boot_id`),
  CONSTRAINT `Ref_125` FOREIGN KEY (`install_id`) REFERENCES `install` (`install_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Ref_203` FOREIGN KEY (`ioc_boot_id`) REFERENCES `ioc_boot` (`ioc_boot_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `iocboot__install`
--

LOCK TABLES `iocboot__install` WRITE;
/*!40000 ALTER TABLE `iocboot__install` DISABLE KEYS */;
/*!40000 ALTER TABLE `iocboot__install` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `iocboot_prop`
--

DROP TABLE IF EXISTS `iocboot_prop`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `iocboot_prop` (
  `iocboot_prop_id` int(11) NOT NULL AUTO_INCREMENT,
  `ioc_boot_id` int(11) DEFAULT NULL,
  `ioc_proptype_id` int(11) DEFAULT NULL,
  `ioc_prop` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`iocboot_prop_id`),
  KEY `Ref_196` (`ioc_proptype_id`),
  KEY `Ref_199` (`ioc_boot_id`),
  CONSTRAINT `Ref_196` FOREIGN KEY (`ioc_proptype_id`) REFERENCES `iocboot_proptype` (`iocboot_proptype_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Ref_199` FOREIGN KEY (`ioc_boot_id`) REFERENCES `ioc_boot` (`ioc_boot_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `iocboot_prop`
--

LOCK TABLES `iocboot_prop` WRITE;
/*!40000 ALTER TABLE `iocboot_prop` DISABLE KEYS */;
/*!40000 ALTER TABLE `iocboot_prop` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `iocboot_proptype`
--

DROP TABLE IF EXISTS `iocboot_proptype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `iocboot_proptype` (
  `iocboot_proptype_id` int(11) NOT NULL AUTO_INCREMENT,
  `iocboot_proptype_name` varchar(50) DEFAULT NULL,
  `iocboot_proptype_desc` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`iocboot_proptype_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `iocboot_proptype`
--

LOCK TABLES `iocboot_proptype` WRITE;
/*!40000 ALTER TABLE `iocboot_proptype` DISABLE KEYS */;
/*!40000 ALTER TABLE `iocboot_proptype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `irmis_version`
--

DROP TABLE IF EXISTS `irmis_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `irmis_version` (
  `irmis_version_id` int(11) NOT NULL AUTO_INCREMENT,
  `irmis_version` varchar(50) DEFAULT NULL,
  `description` text,
  `irmis_version_date` datetime DEFAULT NULL,
  PRIMARY KEY (`irmis_version_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `irmis_version`
--

LOCK TABLES `irmis_version` WRITE;
/*!40000 ALTER TABLE `irmis_version` DISABLE KEYS */;
/*!40000 ALTER TABLE `irmis_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lattice`
--

DROP TABLE IF EXISTS `lattice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lattice` (
  `lattice_id` int(11) NOT NULL AUTO_INCREMENT,
  `model_line_id` int(11) DEFAULT NULL,
  `machine_mode_id` int(11) DEFAULT NULL,
  `model_geometry_id` int(11) DEFAULT NULL,
  `lattice_name` varchar(255) DEFAULT NULL,
  `lattice_version` int(50) DEFAULT NULL,
  `lattice_branch` varchar(50) DEFAULT NULL,
  `lattice_description` varchar(255) DEFAULT NULL,
  `created_by` varchar(45) DEFAULT NULL,
  `create_date` datetime DEFAULT NULL,
  `updated_by` varchar(45) DEFAULT NULL,
  `update_date` datetime DEFAULT NULL,
  PRIMARY KEY (`lattice_id`),
  KEY `FK_model_line` (`model_line_id`),
  KEY `FK_model_geometry` (`model_geometry_id`),
  KEY `FK_machine_mode` (`machine_mode_id`),
  CONSTRAINT `FK_model_line` FOREIGN KEY (`model_line_id`) REFERENCES `model_line` (`model_line_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FK_model_geometry` FOREIGN KEY (`model_geometry_id`) REFERENCES `model_geometry` (`model_geometry_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FK_machine_mode` FOREIGN KEY (`machine_mode_id`) REFERENCES `machine_mode` (`machine_mode_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lattice`
--

LOCK TABLES `lattice` WRITE;
/*!40000 ALTER TABLE `lattice` DISABLE KEYS */;
/*!40000 ALTER TABLE `lattice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `link_detail`
--

DROP TABLE IF EXISTS `link_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `link_detail` (
  `link_detail_id` int(11) NOT NULL AUTO_INCREMENT,
  `install_rel_id` int(11) NOT NULL DEFAULT '0',
  `link_type` int(11) DEFAULT NULL,
  `port_port_connection_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`link_detail_id`),
  KEY `Ref_226` (`install_rel_id`),
  CONSTRAINT `Ref_226` FOREIGN KEY (`install_rel_id`) REFERENCES `install_rel` (`install_rel_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `link_detail`
--

LOCK TABLES `link_detail` WRITE;
/*!40000 ALTER TABLE `link_detail` DISABLE KEYS */;
/*!40000 ALTER TABLE `link_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `machine_mode`
--

DROP TABLE IF EXISTS `machine_mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `machine_mode` (
  `machine_mode_id` int(11) NOT NULL AUTO_INCREMENT,
  `machine_mode_name` varchar(45) DEFAULT NULL,
  `machine_mode_description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`machine_mode_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `machine_mode`
--

LOCK TABLES `machine_mode` WRITE;
/*!40000 ALTER TABLE `machine_mode` DISABLE KEYS */;
/*!40000 ALTER TABLE `machine_mode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `masar_data`
--

DROP TABLE IF EXISTS `masar_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `masar_data` (
  `masar_data_id` int(11) NOT NULL AUTO_INCREMENT,
  `service_event_id` int(11) NOT NULL DEFAULT '0',
  `pv_name` varchar(50) DEFAULT NULL,
  `value` varchar(50) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `severity` int(11) DEFAULT NULL,
  `ioc_timestamp` int(11) unsigned NOT NULL,
  `ioc_timestamp_nano` int(11) unsigned NOT NULL,
  PRIMARY KEY (`masar_data_id`),
  KEY `Ref_10` (`service_event_id`),
  CONSTRAINT `Ref_10` FOREIGN KEY (`service_event_id`) REFERENCES `service_event` (`service_event_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `masar_data`
--

LOCK TABLES `masar_data` WRITE;
/*!40000 ALTER TABLE `masar_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `masar_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `meas_table`
--

DROP TABLE IF EXISTS `meas_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `meas_table` (
  `meas_table_id` int(11) NOT NULL AUTO_INCREMENT,
  `meas_table_name` varchar(50) NOT NULL,
  `meas_desc` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`meas_table_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `meas_table`
--

LOCK TABLES `meas_table` WRITE;
/*!40000 ALTER TABLE `meas_table` DISABLE KEYS */;
/*!40000 ALTER TABLE `meas_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `meas_table_prop`
--

DROP TABLE IF EXISTS `meas_table_prop`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `meas_table_prop` (
  `meas_table_prop_id` int(11) NOT NULL AUTO_INCREMENT,
  `meas_table_id` int(11) DEFAULT NULL,
  `meas_table_prop_name` varchar(50) NOT NULL,
  `meas_table_prop_desc` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`meas_table_prop_id`),
  KEY `Ref_254` (`meas_table_id`),
  CONSTRAINT `Ref_254` FOREIGN KEY (`meas_table_id`) REFERENCES `meas_table` (`meas_table_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `meas_table_prop`
--

LOCK TABLES `meas_table_prop` WRITE;
/*!40000 ALTER TABLE `meas_table_prop` DISABLE KEYS */;
/*!40000 ALTER TABLE `meas_table_prop` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `model`
--

DROP TABLE IF EXISTS `model`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `model` (
  `model_id` int(11) NOT NULL AUTO_INCREMENT,
  `lattice_id` int(11) DEFAULT NULL,
  `model_code_id` int(11) DEFAULT NULL,
  `model_name` varchar(255) DEFAULT NULL,
  `model_desc` varchar(255) DEFAULT NULL,
  `created_by` varchar(45) DEFAULT NULL,
  `create_date` datetime DEFAULT NULL,
  `updated_by` varchar(45) DEFAULT NULL,
  `update_date` datetime DEFAULT NULL,
  `tune_x` double DEFAULT NULL,
  `tune_y` double DEFAULT NULL,
  `chrome_x_0` double DEFAULT NULL,
  `chrome_x_1` double DEFAULT NULL,
  `chrome_x_2` double DEFAULT NULL,
  `chrome_y_0` double DEFAULT NULL,
  `chrome_y_1` double DEFAULT NULL,
  `chrome_y_2` double DEFAULT NULL,
  `final_beam_energy` double DEFAULT NULL,
  PRIMARY KEY (`model_id`),
  KEY `FK_model_code` (`model_code_id`),
  KEY `FK_lattice` (`lattice_id`),
  CONSTRAINT `FK_model_code` FOREIGN KEY (`model_code_id`) REFERENCES `model_code` (`model_code_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FK_lattice` FOREIGN KEY (`lattice_id`) REFERENCES `lattice` (`lattice_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `model`
--

LOCK TABLES `model` WRITE;
/*!40000 ALTER TABLE `model` DISABLE KEYS */;
/*!40000 ALTER TABLE `model` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `model_code`
--

DROP TABLE IF EXISTS `model_code`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `model_code` (
  `model_code_id` int(11) NOT NULL AUTO_INCREMENT,
  `code_name` varchar(45) DEFAULT NULL,
  `algorithm` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`model_code_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `model_code`
--

LOCK TABLES `model_code` WRITE;
/*!40000 ALTER TABLE `model_code` DISABLE KEYS */;
/*!40000 ALTER TABLE `model_code` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `model_geometry`
--

DROP TABLE IF EXISTS `model_geometry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `model_geometry` (
  `model_geometry_id` int(11) NOT NULL AUTO_INCREMENT,
  `model_geometry_name` varchar(45) DEFAULT NULL,
  `model_geometry_description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`model_geometry_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `model_geometry`
--

LOCK TABLES `model_geometry` WRITE;
/*!40000 ALTER TABLE `model_geometry` DISABLE KEYS */;
/*!40000 ALTER TABLE `model_geometry` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `model_line`
--

DROP TABLE IF EXISTS `model_line`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `model_line` (
  `model_line_id` int(11) NOT NULL AUTO_INCREMENT,
  `model_line_name` varchar(45) DEFAULT NULL,
  `model_line_description` varchar(255) DEFAULT NULL,
  `start_position` double DEFAULT NULL,
  `end_position` double DEFAULT NULL,
  `start_marker` varchar(45) DEFAULT NULL,
  `end_marker` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`model_line_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `model_line`
--

LOCK TABLES `model_line` WRITE;
/*!40000 ALTER TABLE `model_line` DISABLE KEYS */;
/*!40000 ALTER TABLE `model_line` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `old_pv`
--

DROP TABLE IF EXISTS `old_pv`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `old_pv` (
  `old_pv_id` int(11) NOT NULL AUTO_INCREMENT,
  `pv_id` int(11) DEFAULT '0',
  `old_pv_name` varchar(50) DEFAULT NULL,
  `old_pv_desc` varchar(255) DEFAULT NULL,
  `old_pv_end_date` datetime DEFAULT NULL,
  PRIMARY KEY (`old_pv_id`),
  KEY `Ref_195` (`pv_id`),
  CONSTRAINT `Ref_195` FOREIGN KEY (`pv_id`) REFERENCES `pv` (`pv_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `old_pv`
--

LOCK TABLES `old_pv` WRITE;
/*!40000 ALTER TABLE `old_pv` DISABLE KEYS */;
/*!40000 ALTER TABLE `old_pv` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `partition_type`
--

DROP TABLE IF EXISTS `partition_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `partition_type` (
  `partition_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `partition_type` varchar(50) DEFAULT NULL,
  `partition_type_description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`partition_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `partition_type`
--

LOCK TABLES `partition_type` WRITE;
/*!40000 ALTER TABLE `partition_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `partition_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `person`
--

DROP TABLE IF EXISTS `person`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `person` (
  `person_id` int(11) NOT NULL AUTO_INCREMENT,
  `last_name` varchar(50) NOT NULL DEFAULT '0',
  `first_name` varchar(50) DEFAULT NULL,
  `telephone` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `bldg` varchar(50) DEFAULT NULL,
  `room` varchar(50) DEFAULT NULL,
  `life_no` int(11) DEFAULT NULL,
  PRIMARY KEY (`person_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `person`
--

LOCK TABLES `person` WRITE;
/*!40000 ALTER TABLE `person` DISABLE KEYS */;
/*!40000 ALTER TABLE `person` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `person__role`
--

DROP TABLE IF EXISTS `person__role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `person__role` (
  `person__role_id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) DEFAULT NULL,
  `max_clearance_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`person__role_id`),
  KEY `Ref_157` (`max_clearance_id`),
  KEY `Ref_160` (`person_id`),
  CONSTRAINT `Ref_157` FOREIGN KEY (`max_clearance_id`) REFERENCES `role` (`role_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Ref_160` FOREIGN KEY (`person_id`) REFERENCES `person` (`person_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `person__role`
--

LOCK TABLES `person__role` WRITE;
/*!40000 ALTER TABLE `person__role` DISABLE KEYS */;
/*!40000 ALTER TABLE `person__role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pin`
--

DROP TABLE IF EXISTS `pin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pin` (
  `pin_id` int(11) NOT NULL AUTO_INCREMENT,
  `port_id` int(11) DEFAULT NULL,
  `signal_source_id` int(11) DEFAULT NULL,
  `pin_designator` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`pin_id`),
  KEY `idx_port_id_pp` (`port_id`),
  KEY `Ref_250` (`signal_source_id`),
  CONSTRAINT `pin_ibfk_2` FOREIGN KEY (`port_id`) REFERENCES `port` (`port_id`),
  CONSTRAINT `Ref_250` FOREIGN KEY (`signal_source_id`) REFERENCES `signal_source` (`signal_source_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pin`
--

LOCK TABLES `pin` WRITE;
/*!40000 ALTER TABLE `pin` DISABLE KEYS */;
/*!40000 ALTER TABLE `pin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `port`
--

DROP TABLE IF EXISTS `port`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `port` (
  `port_id` int(11) NOT NULL AUTO_INCREMENT,
  `cmpnttype__porttype_id` int(11) DEFAULT NULL,
  `install_id` int(11) NOT NULL DEFAULT '0',
  `port_field_label` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`port_id`),
  KEY `idx_port_type_id` (`cmpnttype__porttype_id`),
  KEY `Ref_81` (`install_id`),
  CONSTRAINT `Ref_81` FOREIGN KEY (`install_id`) REFERENCES `install` (`install_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Ref_229` FOREIGN KEY (`cmpnttype__porttype_id`) REFERENCES `cmpnttype__porttype` (`cmpnttype__porttype_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `port`
--

LOCK TABLES `port` WRITE;
/*!40000 ALTER TABLE `port` DISABLE KEYS */;
/*!40000 ALTER TABLE `port` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `port_type`
--

DROP TABLE IF EXISTS `port_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `port_type` (
  `port_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `connector_type` varchar(60) NOT NULL,
  `connector_group` varchar(60) NOT NULL,
  `pin_count` int(11) DEFAULT NULL,
  PRIMARY KEY (`port_type_id`),
  UNIQUE KEY `idx_port_type_group_unique` (`connector_type`,`connector_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `port_type`
--

LOCK TABLES `port_type` WRITE;
/*!40000 ALTER TABLE `port_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `port_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pv`
--

DROP TABLE IF EXISTS `pv`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pv` (
  `pv_id` int(11) NOT NULL AUTO_INCREMENT,
  `pv_name` varchar(128) NOT NULL,
  `description` text,
  PRIMARY KEY (`pv_id`),
  KEY `idx_pv_name` (`pv_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pv`
--

LOCK TABLES `pv` WRITE;
/*!40000 ALTER TABLE `pv` DISABLE KEYS */;
/*!40000 ALTER TABLE `pv` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pv__install`
--

DROP TABLE IF EXISTS `pv__install`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pv__install` (
  `pv__install_id` int(11) NOT NULL AUTO_INCREMENT,
  `pv_id` int(11) NOT NULL DEFAULT '0',
  `install_id` int(11) NOT NULL DEFAULT '0',
  `handle` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`pv__install_id`),
  KEY `idx_pv_id` (`pv_id`),
  KEY `idx_install_id` (`install_id`),
  CONSTRAINT `Ref_111` FOREIGN KEY (`pv_id`) REFERENCES `pv` (`pv_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Ref_116` FOREIGN KEY (`install_id`) REFERENCES `install` (`install_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pv__install`
--

LOCK TABLES `pv__install` WRITE;
/*!40000 ALTER TABLE `pv__install` DISABLE KEYS */;
/*!40000 ALTER TABLE `pv__install` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pv__pvgroup`
--

DROP TABLE IF EXISTS `pv__pvgroup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pv__pvgroup` (
  `pv__pvgroup_id` int(11) NOT NULL AUTO_INCREMENT,
  `pv_id` int(11) NOT NULL DEFAULT '0',
  `pv_group_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`pv__pvgroup_id`),
  KEY `idx_pv_id` (`pv_id`),
  KEY `idx_pvgroup_id` (`pv_group_id`),
  CONSTRAINT `Ref_92` FOREIGN KEY (`pv_id`) REFERENCES `pv` (`pv_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Ref_95` FOREIGN KEY (`pv_group_id`) REFERENCES `pv_group` (`pv_group_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pv__pvgroup`
--

LOCK TABLES `pv__pvgroup` WRITE;
/*!40000 ALTER TABLE `pv__pvgroup` DISABLE KEYS */;
/*!40000 ALTER TABLE `pv__pvgroup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pv_attr`
--

DROP TABLE IF EXISTS `pv_attr`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pv_attr` (
  `pv_attr_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `pv_id` int(11) NOT NULL DEFAULT '0',
  `pv_attrtype_id` int(11) DEFAULT NULL,
  `pv_attr` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`pv_attr_id`),
  KEY `Ref_151` (`pv_id`),
  KEY `Ref_118` (`pv_attrtype_id`),
  CONSTRAINT `Ref_151` FOREIGN KEY (`pv_id`) REFERENCES `pv` (`pv_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Ref_118` FOREIGN KEY (`pv_attrtype_id`) REFERENCES `pv_attrtype` (`pv_attrtype_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pv_attr`
--

LOCK TABLES `pv_attr` WRITE;
/*!40000 ALTER TABLE `pv_attr` DISABLE KEYS */;
/*!40000 ALTER TABLE `pv_attr` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pv_attrtype`
--

DROP TABLE IF EXISTS `pv_attrtype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pv_attrtype` (
  `pv_attrtype_id` int(11) NOT NULL AUTO_INCREMENT,
  `pv_attrtype_name` varchar(50) DEFAULT NULL,
  `pv_attrtype_desc` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`pv_attrtype_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pv_attrtype`
--

LOCK TABLES `pv_attrtype` WRITE;
/*!40000 ALTER TABLE `pv_attrtype` DISABLE KEYS */;
/*!40000 ALTER TABLE `pv_attrtype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pv_group`
--

DROP TABLE IF EXISTS `pv_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pv_group` (
  `pv_group_id` int(11) NOT NULL AUTO_INCREMENT,
  `pv_group_name` varchar(50) DEFAULT NULL,
  `pv_group_func` varchar(50) DEFAULT NULL,
  `pvg_creation_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `pvg_version` varchar(50) DEFAULT NULL,
  `pvg_version_desc` varchar(255) DEFAULT NULL,
  `pvg_status` enum('in progress','complete','invalid') DEFAULT NULL,
  PRIMARY KEY (`pv_group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pv_group`
--

LOCK TABLES `pv_group` WRITE;
/*!40000 ALTER TABLE `pv_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `pv_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pv_rel`
--

DROP TABLE IF EXISTS `pv_rel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pv_rel` (
  `pv_rel_id` int(11) NOT NULL AUTO_INCREMENT,
  `rel_type` varchar(50) DEFAULT NULL,
  `parent_pv_id` int(11) NOT NULL DEFAULT '0',
  `child_pv_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`pv_rel_id`),
  KEY `Ref_154` (`parent_pv_id`),
  KEY `Ref_155` (`child_pv_id`),
  CONSTRAINT `Ref_154` FOREIGN KEY (`parent_pv_id`) REFERENCES `pv` (`pv_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Ref_155` FOREIGN KEY (`child_pv_id`) REFERENCES `pv` (`pv_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pv_rel`
--

LOCK TABLES `pv_rel` WRITE;
/*!40000 ALTER TABLE `pv_rel` DISABLE KEYS */;
/*!40000 ALTER TABLE `pv_rel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pvgroup__serviceconfig`
--

DROP TABLE IF EXISTS `pvgroup__serviceconfig`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pvgroup__serviceconfig` (
  `pvgroup__serviceconfig_id` int(11) NOT NULL AUTO_INCREMENT,
  `pv_group_id` int(11) NOT NULL DEFAULT '0',
  `service_config_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`pvgroup__serviceconfig_id`),
  KEY `Ref_09` (`service_config_id`),
  KEY `Ref_137` (`pv_group_id`),
  CONSTRAINT `Ref_09` FOREIGN KEY (`service_config_id`) REFERENCES `service_config` (`service_config_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Ref_137` FOREIGN KEY (`pv_group_id`) REFERENCES `pv_group` (`pv_group_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pvgroup__serviceconfig`
--

LOCK TABLES `pvgroup__serviceconfig` WRITE;
/*!40000 ALTER TABLE `pvgroup__serviceconfig` DISABLE KEYS */;
/*!40000 ALTER TABLE `pvgroup__serviceconfig` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rec`
--

DROP TABLE IF EXISTS `rec`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rec` (
  `rec_id` int(11) NOT NULL AUTO_INCREMENT,
  `ioc_boot_id` int(11) DEFAULT NULL,
  `rec_nm` varchar(128) DEFAULT NULL,
  `rec_type_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`rec_id`),
  KEY `idx_rec_nm` (`rec_nm`),
  KEY `idx_ioc_boot_id` (`ioc_boot_id`),
  KEY `idx_rec_type_id` (`rec_type_id`),
  CONSTRAINT `rec_ibfk_1` FOREIGN KEY (`ioc_boot_id`) REFERENCES `ioc_boot` (`ioc_boot_id`),
  CONSTRAINT `rec_ibfk_2` FOREIGN KEY (`rec_type_id`) REFERENCES `rec_type` (`rec_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rec`
--

LOCK TABLES `rec` WRITE;
/*!40000 ALTER TABLE `rec` DISABLE KEYS */;
/*!40000 ALTER TABLE `rec` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rec_alias`
--

DROP TABLE IF EXISTS `rec_alias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rec_alias` (
  `rec_alias_id` int(11) NOT NULL AUTO_INCREMENT,
  `rec_id` int(11) DEFAULT NULL,
  `alias_nm` varchar(50) DEFAULT NULL,
  `ioc_resource_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`rec_alias_id`),
  KEY `Ref_205` (`rec_id`),
  KEY `Ref_206` (`ioc_resource_id`),
  CONSTRAINT `Ref_205` FOREIGN KEY (`rec_id`) REFERENCES `rec` (`rec_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Ref_206` FOREIGN KEY (`ioc_resource_id`) REFERENCES `ioc_resource` (`ioc_resource_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rec_alias`
--

LOCK TABLES `rec_alias` WRITE;
/*!40000 ALTER TABLE `rec_alias` DISABLE KEYS */;
/*!40000 ALTER TABLE `rec_alias` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rec_client`
--

DROP TABLE IF EXISTS `rec_client`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rec_client` (
  `rec_client_id` int(11) NOT NULL AUTO_INCREMENT,
  `rec_client_type_id` int(11) DEFAULT NULL,
  `rec_nm` varchar(128) DEFAULT NULL,
  `fld_type` varchar(24) DEFAULT NULL,
  `vuri_id` int(11) DEFAULT NULL,
  `current_load` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`rec_client_id`),
  KEY `idx_rec_nm` (`rec_nm`),
  KEY `FKIndex1` (`rec_client_type_id`),
  KEY `idx_vuri_id` (`vuri_id`),
  CONSTRAINT `Ref_84` FOREIGN KEY (`rec_client_type_id`) REFERENCES `rec_client_type` (`rec_client_type_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Ref_86` FOREIGN KEY (`vuri_id`) REFERENCES `vuri` (`vuri_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rec_client`
--

LOCK TABLES `rec_client` WRITE;
/*!40000 ALTER TABLE `rec_client` DISABLE KEYS */;
/*!40000 ALTER TABLE `rec_client` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rec_client_type`
--

DROP TABLE IF EXISTS `rec_client_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rec_client_type` (
  `rec_client_type_id` int(11) NOT NULL,
  `description` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`rec_client_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rec_client_type`
--

LOCK TABLES `rec_client_type` WRITE;
/*!40000 ALTER TABLE `rec_client_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `rec_client_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rec_type`
--

DROP TABLE IF EXISTS `rec_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rec_type` (
  `rec_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `ioc_boot_id` int(11) DEFAULT NULL,
  `rec_type` varchar(24) DEFAULT NULL,
  `ioc_resource_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`rec_type_id`),
  KEY `idx_ioc_boot_id` (`ioc_boot_id`),
  KEY `idx_ioc_resource_id` (`ioc_resource_id`),
  CONSTRAINT `rec_type_ibfk_1` FOREIGN KEY (`ioc_boot_id`) REFERENCES `ioc_boot` (`ioc_boot_id`),
  CONSTRAINT `rec_type_ibfk_2` FOREIGN KEY (`ioc_resource_id`) REFERENCES `ioc_resource` (`ioc_resource_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rec_type`
--

LOCK TABLES `rec_type` WRITE;
/*!40000 ALTER TABLE `rec_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `rec_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rec_type_dev_sup`
--

DROP TABLE IF EXISTS `rec_type_dev_sup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rec_type_dev_sup` (
  `rec_type_dev_sup_id` int(11) NOT NULL AUTO_INCREMENT,
  `rec_type_id` int(11) DEFAULT NULL,
  `dtyp_str` varchar(24) DEFAULT NULL,
  `dev_sup_dset` varchar(50) DEFAULT NULL,
  `dev_sup_io_type` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`rec_type_dev_sup_id`),
  KEY `Ref_228` (`rec_type_id`),
  CONSTRAINT `Ref_228` FOREIGN KEY (`rec_type_id`) REFERENCES `rec_type` (`rec_type_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rec_type_dev_sup`
--

LOCK TABLES `rec_type_dev_sup` WRITE;
/*!40000 ALTER TABLE `rec_type_dev_sup` DISABLE KEYS */;
/*!40000 ALTER TABLE `rec_type_dev_sup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `role` (
  `role_id` int(11) NOT NULL AUTO_INCREMENT,
  `role` varchar(50) DEFAULT NULL,
  `clearance` int(11) DEFAULT NULL,
  `role_description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`role_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rot_coil_data`
--

DROP TABLE IF EXISTS `rot_coil_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rot_coil_data` (
  `rot_coil_data_id` int(11) NOT NULL AUTO_INCREMENT,
  `inventory_id` int(11) NOT NULL DEFAULT '0',
  `alias` varchar(50) DEFAULT NULL,
  `meas_coil_id` varchar(50) DEFAULT NULL,
  `ref_radius` double DEFAULT NULL,
  `magnet_notes` varchar(50) DEFAULT NULL,
  `login_name` varchar(2000) DEFAULT NULL,
  `cond_curr` double DEFAULT NULL,
  `meas_loc` varchar(50) DEFAULT NULL,
  `run_number` varchar(50) DEFAULT NULL,
  `sub_device` varchar(50) DEFAULT NULL,
  `current_1` double DEFAULT NULL,
  `current_2` double DEFAULT NULL,
  `current_3` double DEFAULT NULL,
  `up_dn_1` varchar(50) DEFAULT NULL,
  `up_dn_2` varchar(50) DEFAULT NULL,
  `up_dn_3` varchar(50) DEFAULT NULL,
  `analysis_number` varchar(50) DEFAULT NULL,
  `integral_xfer_function` double DEFAULT NULL,
  `orig_offset_x` double DEFAULT NULL,
  `orig_offset_y` double DEFAULT NULL,
  `B_ref_int` double DEFAULT NULL,
  `Roll_angle` double DEFAULT NULL,
  `meas_notes` varchar(2000) DEFAULT NULL,
  `meas_date` datetime DEFAULT NULL,
  `author` varchar(50) DEFAULT NULL,
  `a1` double DEFAULT NULL,
  `a2` double DEFAULT NULL,
  `a3` double DEFAULT NULL,
  `b1` double DEFAULT NULL,
  `b2` double DEFAULT NULL,
  `b3` double DEFAULT NULL,
  `a4_21` varchar(255) DEFAULT NULL,
  `b4_21` varchar(255) DEFAULT NULL,
  `data_issues` varchar(50) DEFAULT NULL,
  `data_usage` int(11) DEFAULT NULL,
  PRIMARY KEY (`rot_coil_data_id`),
  KEY `Ref_192` (`inventory_id`),
  CONSTRAINT `Ref_192` FOREIGN KEY (`inventory_id`) REFERENCES `inventory` (`inventory_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rot_coil_data`
--

LOCK TABLES `rot_coil_data` WRITE;
/*!40000 ALTER TABLE `rot_coil_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `rot_coil_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `service`
--

DROP TABLE IF EXISTS `service`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `service` (
  `service_id` int(11) NOT NULL AUTO_INCREMENT,
  `service_name` varchar(50) DEFAULT NULL,
  `service_desc` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`service_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `service`
--

LOCK TABLES `service` WRITE;
/*!40000 ALTER TABLE `service` DISABLE KEYS */;
/*!40000 ALTER TABLE `service` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `service__role`
--

DROP TABLE IF EXISTS `service__role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `service__role` (
  `service__role_id` int(11) NOT NULL AUTO_INCREMENT,
  `service_id` int(11) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`service__role_id`),
  KEY `Ref_173` (`role_id`),
  KEY `Ref_171` (`service_id`),
  CONSTRAINT `Ref_173` FOREIGN KEY (`role_id`) REFERENCES `role` (`role_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Ref_171` FOREIGN KEY (`service_id`) REFERENCES `service` (`service_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `service__role`
--

LOCK TABLES `service__role` WRITE;
/*!40000 ALTER TABLE `service__role` DISABLE KEYS */;
/*!40000 ALTER TABLE `service__role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `service_config`
--

DROP TABLE IF EXISTS `service_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `service_config` (
  `service_config_id` int(11) NOT NULL AUTO_INCREMENT,
  `service_id` int(11) NOT NULL DEFAULT '0',
  `service_config_name` varchar(50) DEFAULT NULL,
  `service_config_desc` varchar(255) DEFAULT NULL,
  `service_config_version` int(11) DEFAULT NULL,
  `service_config_create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`service_config_id`),
  KEY `Ref_197` (`service_id`),
  CONSTRAINT `Ref_197` FOREIGN KEY (`service_id`) REFERENCES `service` (`service_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `service_config`
--

LOCK TABLES `service_config` WRITE;
/*!40000 ALTER TABLE `service_config` DISABLE KEYS */;
/*!40000 ALTER TABLE `service_config` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `service_config_prop`
--

DROP TABLE IF EXISTS `service_config_prop`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `service_config_prop` (
  `service_config_prop_id` int(11) NOT NULL AUTO_INCREMENT,
  `service_config_id` int(11) NOT NULL DEFAULT '0',
  `service_config_prop_name` varchar(2555) DEFAULT NULL,
  `service_config_prop_value` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`service_config_prop_id`),
  KEY `Ref_12` (`service_config_id`),
  CONSTRAINT `Ref_12` FOREIGN KEY (`service_config_id`) REFERENCES `service_config` (`service_config_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `service_config_prop`
--

LOCK TABLES `service_config_prop` WRITE;
/*!40000 ALTER TABLE `service_config_prop` DISABLE KEYS */;
/*!40000 ALTER TABLE `service_config_prop` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `service_event`
--

DROP TABLE IF EXISTS `service_event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `service_event` (
  `service_event_id` int(11) NOT NULL AUTO_INCREMENT,
  `service_config_id` int(11) NOT NULL DEFAULT '0',
  `service_event_user_tag` varchar(255) DEFAULT NULL,
  `service_event_UTC_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `service_event_serial_tag` int(11) DEFAULT '0',
  PRIMARY KEY (`service_event_id`),
  KEY `Ref_08` (`service_config_id`),
  CONSTRAINT `Ref_08` FOREIGN KEY (`service_config_id`) REFERENCES `service_config` (`service_config_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `service_event`
--

LOCK TABLES `service_event` WRITE;
/*!40000 ALTER TABLE `service_event` DISABLE KEYS */;
/*!40000 ALTER TABLE `service_event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `service_event_prop`
--

DROP TABLE IF EXISTS `service_event_prop`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `service_event_prop` (
  `service_event_prop_id` int(11) NOT NULL AUTO_INCREMENT,
  `service_event_id` int(11) NOT NULL DEFAULT '0',
  `service_event_prop_name` varchar(255) DEFAULT NULL,
  `service_event_prop_value` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`service_event_prop_id`),
  KEY `Ref_11` (`service_event_id`),
  CONSTRAINT `Ref_11` FOREIGN KEY (`service_event_id`) REFERENCES `service_event` (`service_event_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `service_event_prop`
--

LOCK TABLES `service_event_prop` WRITE;
/*!40000 ALTER TABLE `service_event_prop` DISABLE KEYS */;
/*!40000 ALTER TABLE `service_event_prop` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `signal_desc`
--

DROP TABLE IF EXISTS `signal_desc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `signal_desc` (
  `signal_desc_id` int(11) NOT NULL AUTO_INCREMENT,
  `signal_type_id` int(11) DEFAULT NULL,
  `signal_quality_id` int(11) NOT NULL,
  PRIMARY KEY (`signal_desc_id`),
  KEY `Ref_248` (`signal_type_id`),
  KEY `Ref_249` (`signal_quality_id`),
  CONSTRAINT `Ref_248` FOREIGN KEY (`signal_type_id`) REFERENCES `signal_type` (`signal_type_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Ref_249` FOREIGN KEY (`signal_quality_id`) REFERENCES `signal_quality` (`signal_quality_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `signal_desc`
--

LOCK TABLES `signal_desc` WRITE;
/*!40000 ALTER TABLE `signal_desc` DISABLE KEYS */;
/*!40000 ALTER TABLE `signal_desc` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `signal_quality`
--

DROP TABLE IF EXISTS `signal_quality`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `signal_quality` (
  `signal_quality_id` int(11) NOT NULL AUTO_INCREMENT,
  `signal_quality` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`signal_quality_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `signal_quality`
--

LOCK TABLES `signal_quality` WRITE;
/*!40000 ALTER TABLE `signal_quality` DISABLE KEYS */;
/*!40000 ALTER TABLE `signal_quality` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `signal_source`
--

DROP TABLE IF EXISTS `signal_source`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `signal_source` (
  `signal_source_id` int(11) NOT NULL AUTO_INCREMENT,
  `signal_source` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`signal_source_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `signal_source`
--

LOCK TABLES `signal_source` WRITE;
/*!40000 ALTER TABLE `signal_source` DISABLE KEYS */;
/*!40000 ALTER TABLE `signal_source` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `signal_type`
--

DROP TABLE IF EXISTS `signal_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `signal_type` (
  `signal_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `signal_type` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`signal_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `signal_type`
--

LOCK TABLES `signal_type` WRITE;
/*!40000 ALTER TABLE `signal_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `signal_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `task`
--

DROP TABLE IF EXISTS `task`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `task` (
  `task_id` int(11) NOT NULL AUTO_INCREMENT,
  `workflow_id` int(11) NOT NULL DEFAULT '0',
  `task_tmplt_id` int(11) NOT NULL DEFAULT '0',
  `task_start_date` datetime DEFAULT NULL,
  `task_completion_date` datetime DEFAULT NULL,
  `task_status` int(11) DEFAULT NULL,
  `task_done_by` varchar(50) NOT NULL DEFAULT '0',
  PRIMARY KEY (`task_id`),
  KEY `Ref_168` (`workflow_id`),
  KEY `Ref_239` (`task_tmplt_id`),
  CONSTRAINT `Ref_168` FOREIGN KEY (`workflow_id`) REFERENCES `workflow` (`workflow_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Ref_239` FOREIGN KEY (`task_tmplt_id`) REFERENCES `task_tmplt` (`task_tmplt_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task`
--

LOCK TABLES `task` WRITE;
/*!40000 ALTER TABLE `task` DISABLE KEYS */;
/*!40000 ALTER TABLE `task` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `task__document`
--

DROP TABLE IF EXISTS `task__document`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `task__document` (
  `task__document_id` int(11) NOT NULL AUTO_INCREMENT,
  `task_id` int(11) NOT NULL DEFAULT '0',
  `document_id` int(11) DEFAULT NULL,
  `dr` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`task__document_id`),
  KEY `Ref_235` (`document_id`),
  KEY `Ref_234` (`task_id`),
  CONSTRAINT `Ref_235` FOREIGN KEY (`document_id`) REFERENCES `document` (`document_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Ref_234` FOREIGN KEY (`task_id`) REFERENCES `task` (`task_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task__document`
--

LOCK TABLES `task__document` WRITE;
/*!40000 ALTER TABLE `task__document` DISABLE KEYS */;
/*!40000 ALTER TABLE `task__document` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `task__elogentry`
--

DROP TABLE IF EXISTS `task__elogentry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `task__elogentry` (
  `task__elogentry_id` int(11) NOT NULL AUTO_INCREMENT,
  `task_id` int(11) NOT NULL DEFAULT '0',
  `elog_entry_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`task__elogentry_id`),
  KEY `Ref_183` (`task_id`),
  KEY `Ref_194` (`elog_entry_id`),
  CONSTRAINT `Ref_183` FOREIGN KEY (`task_id`) REFERENCES `task` (`task_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Ref_194` FOREIGN KEY (`elog_entry_id`) REFERENCES `elog_entry` (`elog_entry_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task__elogentry`
--

LOCK TABLES `task__elogentry` WRITE;
/*!40000 ALTER TABLE `task__elogentry` DISABLE KEYS */;
/*!40000 ALTER TABLE `task__elogentry` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `task_tmplt`
--

DROP TABLE IF EXISTS `task_tmplt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `task_tmplt` (
  `task_tmplt_id` int(11) NOT NULL AUTO_INCREMENT,
  `workflow_tmplt_id` int(11) NOT NULL DEFAULT '0',
  `task_op` varchar(50) NOT NULL DEFAULT '0',
  `task_description` text,
  `task_order` int(11) DEFAULT NULL,
  `task_lock` int(11) DEFAULT NULL,
  PRIMARY KEY (`task_tmplt_id`),
  KEY `Ref_232` (`workflow_tmplt_id`),
  CONSTRAINT `Ref_232` FOREIGN KEY (`workflow_tmplt_id`) REFERENCES `workflow_tmplt` (`workflow_tmplt_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task_tmplt`
--

LOCK TABLES `task_tmplt` WRITE;
/*!40000 ALTER TABLE `task_tmplt` DISABLE KEYS */;
/*!40000 ALTER TABLE `task_tmplt` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `uri`
--

DROP TABLE IF EXISTS `uri`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `uri` (
  `uri_id` int(11) NOT NULL AUTO_INCREMENT,
  `uri` varchar(255) DEFAULT NULL,
  `uri_modified_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `modified_by` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`uri_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `uri`
--

LOCK TABLES `uri` WRITE;
/*!40000 ALTER TABLE `uri` DISABLE KEYS */;
/*!40000 ALTER TABLE `uri` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendor`
--

DROP TABLE IF EXISTS `vendor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vendor` (
  `vendor_id` int(11) NOT NULL AUTO_INCREMENT,
  `vendor_name` varchar(100) NOT NULL,
  `vendor_description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`vendor_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendor`
--

LOCK TABLES `vendor` WRITE;
/*!40000 ALTER TABLE `vendor` DISABLE KEYS */;
INSERT INTO `vendor` VALUES (1,'Everson-Tesla, USA',NULL),(2,'BINP, Russia',NULL),(3,'Tesla, England',NULL),(4,'Buckley, New Zealand',NULL),(5,'IHEP, China',NULL),(6,'Danfysik, Denmark',NULL),(7,'RI',NULL),(8,'Stangenes, USA',NULL);
/*!40000 ALTER TABLE `vendor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vuri`
--

DROP TABLE IF EXISTS `vuri`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vuri` (
  `vuri_id` int(11) NOT NULL AUTO_INCREMENT,
  `uri_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`vuri_id`),
  KEY `idx_uri_id` (`uri_id`),
  CONSTRAINT `Ref_50` FOREIGN KEY (`uri_id`) REFERENCES `uri` (`uri_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vuri`
--

LOCK TABLES `vuri` WRITE;
/*!40000 ALTER TABLE `vuri` DISABLE KEYS */;
/*!40000 ALTER TABLE `vuri` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vuri_rel`
--

DROP TABLE IF EXISTS `vuri_rel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vuri_rel` (
  `vuri_rel_id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_vuri_id` int(11) DEFAULT NULL,
  `child_vuri_id` int(11) DEFAULT NULL,
  `rel_info` text,
  PRIMARY KEY (`vuri_rel_id`),
  KEY `idx_parent_vuri_id` (`parent_vuri_id`),
  KEY `idx_child_vuri_id` (`child_vuri_id`),
  CONSTRAINT `Ref_51` FOREIGN KEY (`parent_vuri_id`) REFERENCES `vuri` (`vuri_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Ref_64` FOREIGN KEY (`child_vuri_id`) REFERENCES `vuri` (`vuri_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vuri_rel`
--

LOCK TABLES `vuri_rel` WRITE;
/*!40000 ALTER TABLE `vuri_rel` DISABLE KEYS */;
/*!40000 ALTER TABLE `vuri_rel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workflow`
--

DROP TABLE IF EXISTS `workflow`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `workflow` (
  `workflow_id` int(11) NOT NULL AUTO_INCREMENT,
  `workflow_tmplt_id` int(11) DEFAULT NULL,
  `workflow_no` varchar(50) NOT NULL DEFAULT '0',
  `workflow_start_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `workflow_completion_date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `workflow_status` enum('Not Started','In Progress','Blocked','Void','Complete') DEFAULT NULL,
  `workflow_create_date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`workflow_id`),
  KEY `Ref_233` (`workflow_tmplt_id`),
  CONSTRAINT `Ref_233` FOREIGN KEY (`workflow_tmplt_id`) REFERENCES `workflow_tmplt` (`workflow_tmplt_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workflow`
--

LOCK TABLES `workflow` WRITE;
/*!40000 ALTER TABLE `workflow` DISABLE KEYS */;
/*!40000 ALTER TABLE `workflow` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workflow__inventory`
--

DROP TABLE IF EXISTS `workflow__inventory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `workflow__inventory` (
  `workflow__inventory` int(11) NOT NULL AUTO_INCREMENT,
  `workflow_id` int(11) DEFAULT NULL,
  `inventory_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`workflow__inventory`),
  KEY `Ref_153` (`inventory_id`),
  KEY `Ref_156` (`workflow_id`),
  CONSTRAINT `Ref_153` FOREIGN KEY (`inventory_id`) REFERENCES `inventory` (`inventory_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Ref_156` FOREIGN KEY (`workflow_id`) REFERENCES `workflow` (`workflow_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workflow__inventory`
--

LOCK TABLES `workflow__inventory` WRITE;
/*!40000 ALTER TABLE `workflow__inventory` DISABLE KEYS */;
/*!40000 ALTER TABLE `workflow__inventory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workflow__person`
--

DROP TABLE IF EXISTS `workflow__person`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `workflow__person` (
  `workflow__person_id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) DEFAULT '0',
  `workflow_id` int(11) DEFAULT '0',
  `role_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`workflow__person_id`),
  KEY `Ref_04` (`workflow_id`),
  KEY `Ref_170` (`person_id`),
  KEY `Ref_176` (`role_id`),
  CONSTRAINT `Ref_04` FOREIGN KEY (`workflow_id`) REFERENCES `workflow` (`workflow_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Ref_170` FOREIGN KEY (`person_id`) REFERENCES `person` (`person_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `Ref_176` FOREIGN KEY (`role_id`) REFERENCES `role` (`role_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workflow__person`
--

LOCK TABLES `workflow__person` WRITE;
/*!40000 ALTER TABLE `workflow__person` DISABLE KEYS */;
/*!40000 ALTER TABLE `workflow__person` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workflow_tmplt`
--

DROP TABLE IF EXISTS `workflow_tmplt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `workflow_tmplt` (
  `workflow_tmplt_id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(50) DEFAULT NULL,
  `workflow_description` varchar(255) DEFAULT NULL,
  `revision` varchar(50) DEFAULT NULL,
  `revision_date` datetime DEFAULT NULL,
  `requires_inventory` enum('none','one','one or more','zero or more','zero or one') DEFAULT NULL,
  `recurring_period_number` int(11) DEFAULT NULL,
  `recurring_period_unit` varchar(50) DEFAULT NULL,
  `workflow_type_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`workflow_tmplt_id`),
  KEY `Ref_251` (`workflow_type_id`),
  CONSTRAINT `Ref_251` FOREIGN KEY (`workflow_type_id`) REFERENCES `workflow_type` (`workflow_type_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workflow_tmplt`
--

LOCK TABLES `workflow_tmplt` WRITE;
/*!40000 ALTER TABLE `workflow_tmplt` DISABLE KEYS */;
/*!40000 ALTER TABLE `workflow_tmplt` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workflow_tmplt_hdr`
--

DROP TABLE IF EXISTS `workflow_tmplt_hdr`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `workflow_tmplt_hdr` (
  `workflow_tmplt_hdr_id` int(11) NOT NULL AUTO_INCREMENT,
  `workflow_tmplt_id` int(11) NOT NULL DEFAULT '0',
  `workflow_tmplt_hdr_text` varchar(50) DEFAULT NULL,
  `workflow_tmplt_hdr_content` text NOT NULL,
  `workflow_tmplt_hdr_order` int(11) DEFAULT NULL,
  `workflow_tmplt_hdr_description` text,
  `sign_off_required` int(11) DEFAULT NULL,
  PRIMARY KEY (`workflow_tmplt_hdr_id`),
  KEY `Ref_231` (`workflow_tmplt_id`),
  CONSTRAINT `Ref_231` FOREIGN KEY (`workflow_tmplt_id`) REFERENCES `workflow_tmplt` (`workflow_tmplt_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workflow_tmplt_hdr`
--

LOCK TABLES `workflow_tmplt_hdr` WRITE;
/*!40000 ALTER TABLE `workflow_tmplt_hdr` DISABLE KEYS */;
/*!40000 ALTER TABLE `workflow_tmplt_hdr` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workflow_type`
--

DROP TABLE IF EXISTS `workflow_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `workflow_type` (
  `workflow_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `workflow_type` varchar(50) NOT NULL DEFAULT '0',
  `workflow_type_description` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`workflow_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workflow_type`
--

LOCK TABLES `workflow_type` WRITE;
/*!40000 ALTER TABLE `workflow_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `workflow_type` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2013-03-06 14:10:01