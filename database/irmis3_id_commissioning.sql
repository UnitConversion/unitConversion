-- =============================================================================
-- Diagram Name: v0.3
-- Created on: 1/8/2014 10:22:43 AM
-- Diagram Version: 41
-- =============================================================================
SET FOREIGN_KEY_CHECKS=0;

-- Drop table cmpnt_type
DROP TABLE IF EXISTS `cmpnt_type`;

CREATE TABLE `cmpnt_type` (
  `cmpnt_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` varchar(100),
  PRIMARY KEY(`cmpnt_type_id`)
)
ENGINE=INNODB
CHARACTER SET latin1 
COLLATE latin1_swedish_ci ;

-- Drop table vendor
DROP TABLE IF EXISTS `vendor`;

CREATE TABLE `vendor` (
  `vendor_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100),
  PRIMARY KEY(`vendor_id`)
)
ENGINE=INNODB;

-- Drop table id_raw_data
DROP TABLE IF EXISTS `id_raw_data`;

CREATE TABLE `id_raw_data` (
  `id_raw_data_id` int(11) NOT NULL AUTO_INCREMENT,
  `data` blob,
  PRIMARY KEY(`id_raw_data_id`)
)
ENGINE=INNODB;

-- Drop table install_rel_prop_type
DROP TABLE IF EXISTS `install_rel_prop_type`;

CREATE TABLE `install_rel_prop_type` (
  `install_rel_prop_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `install_rel_prop_type_name` varchar(50),
  `install_rel_prop_type_desc` varchar(50),
  `install_rel_prop_type_units` varchar(50),
  PRIMARY KEY(`install_rel_prop_type_id`)
)
ENGINE=INNODB
CHECKSUM = 1
PACK_KEYS = 1;

-- Drop table id_data_method
DROP TABLE IF EXISTS `id_data_method`;

CREATE TABLE `id_data_method` (
  `id_data_method_id` int(11) NOT NULL AUTO_INCREMENT,
  `method_name` varchar(255),
  `description` varchar(255),
  PRIMARY KEY(`id_data_method_id`)
)
ENGINE=INNODB;

-- Drop table install
DROP TABLE IF EXISTS `install`;

CREATE TABLE `install` (
  `install_id` int(11) NOT NULL AUTO_INCREMENT,
  `cmpnt_type_id` int(11) NOT NULL,
  `field_name` varchar(100) NOT NULL,
  `location` varchar(255),
  `coordinate_center` float,
  PRIMARY KEY(`install_id`),
  UNIQUE INDEX `field_name`(`field_name`),
  INDEX `FKIndex1`(`cmpnt_type_id`),
  CONSTRAINT `(cmpnt_type_id=cmpnt_type_id)` FOREIGN KEY (`cmpnt_type_id`)
    REFERENCES `cmpnt_type`(`cmpnt_type_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB
CHARACTER SET latin1 
COLLATE latin1_swedish_ci ;

-- Drop table install_rel
DROP TABLE IF EXISTS `install_rel`;

CREATE TABLE `install_rel` (
  `install_rel_id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_install_id` int(11) NOT NULL DEFAULT '0',
  `child_install_id` int(11) NOT NULL DEFAULT '0',
  `install_rel_type_id` int(11),
  `logical_desc` varchar(60),
  `logical_order` int(11),
  `install_date` datetime,
  PRIMARY KEY(`install_rel_id`),
  INDEX `FKIndex1`(`parent_install_id`),
  INDEX `FKIndex2`(`child_install_id`),
  CONSTRAINT `(install_id=parent_install_id)` FOREIGN KEY (`parent_install_id`)
    REFERENCES `install`(`install_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `(install_id=child_install_id)` FOREIGN KEY (`child_install_id`)
    REFERENCES `install`(`install_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table inventory
DROP TABLE IF EXISTS `inventory`;

CREATE TABLE `inventory` (
  `inventory_id` int(11) NOT NULL AUTO_INCREMENT,
  `cmpnt_type_id` int(11),
  `vendor_id` int(11) NOT NULL DEFAULT '0',
  `name` varchar(100) NOT NULL,
  `alias` varchar(100),
  `serial_no` varchar(50),
  PRIMARY KEY(`inventory_id`),
  INDEX `FKIndex1`(`vendor_id`),
  INDEX `FKIndex2`(`cmpnt_type_id`),
  CONSTRAINT `(vendor_id=vendor_id)` FOREIGN KEY (`vendor_id`)
    REFERENCES `vendor`(`vendor_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `(cmpnt_type_id=cmpnt_type_id )` FOREIGN KEY (`cmpnt_type_id`)
    REFERENCES `cmpnt_type`(`cmpnt_type_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB
CHARACTER SET latin1 
COLLATE latin1_swedish_ci ;

-- Drop table id_offline_data
DROP TABLE IF EXISTS `id_offline_data`;

CREATE TABLE `id_offline_data` (
  `id_offline_data_id` int(11) NOT NULL AUTO_INCREMENT,
  `inventory_id` int(11) NOT NULL,
  `id_data_method_id` int(11) NOT NULL,
  `id_raw_data_id` int(11) NOT NULL DEFAULT '0',
  `login_name` varchar(255),
  `description` varchar(4096),
  `date` datetime,
  `gap` float,
  `phase1` float,
  `phase2` float,
  `phase3` float,
  `phase4` float,
  `phase_mode` varchar(2),
  `polar_mode` varchar(4),
  `data_status` tinyint(4) NOT NULL DEFAULT '1',
  `result_file_name` varchar(255) NOT NULL,
  `result_file_time` datetime,
  `script_file_name` varchar(255),
  `script_file_content` mediumtext,
  PRIMARY KEY(`id_offline_data_id`),
  INDEX `FKIndex1`(`id_data_method_id`),
  INDEX `FKIndex2`(`inventory_id`),
  INDEX `FKIndex3`(`id_raw_data_id`),
  CONSTRAINT `(id_data_method_id= id_data_method_id)` FOREIGN KEY (`id_data_method_id`)
    REFERENCES `id_data_method`(`id_data_method_id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `(inventory_id = inventory_id)` FOREIGN KEY (`inventory_id`)
    REFERENCES `inventory`(`inventory_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `(id_raw_data_id=id_raw_data_id)` FOREIGN KEY (`id_raw_data_id`)
    REFERENCES `id_raw_data`(`id_raw_data_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB
CHARACTER SET latin1 
COLLATE latin1_swedish_ci ;

-- Drop table inventory_prop
DROP TABLE IF EXISTS `inventory_prop`;

CREATE TABLE `inventory_prop` (
  `inventory_prop_id` int(11) NOT NULL AUTO_INCREMENT,
  `inventory_id` int(11),
  `length` float,
  `up_corrector_position` float(9,3),
  `middle_corrector_position` float(9,3),
  `down_corrector_position` float,
  `gap_min` float,
  `gap_max` float,
  `gap_tolerance` float,
  `phase1_min` float,
  `phase1_max` float,
  `phase2_min` float,
  `phase2_max` float,
  `phase3_min` float,
  `phase3_max` float,
  `phase4_min` float,
  `phase4_max` float,
  `phase_tolerance` float,
  `k_max_linear` float,
  `k_max_circular` float,
  `phase_mode_p` varchar(1),
  `phase_mode_a1` varchar(1),
  `phase_mode_a2` varchar(1),
  PRIMARY KEY(`inventory_prop_id`),
  INDEX `FKIndex1`(`inventory_id`),
  CONSTRAINT `(inventory_id=inventory_id)` FOREIGN KEY (`inventory_id`)
    REFERENCES `inventory`(`inventory_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB
CHARACTER SET latin1 
COLLATE latin1_swedish_ci ;

-- Drop table id_online_data
DROP TABLE IF EXISTS `id_online_data`;

CREATE TABLE `id_online_data` (
  `id_online_data_id` int(11) NOT NULL AUTO_INCREMENT,
  `install_id` int(11) NOT NULL DEFAULT '0',
  `login_name` varchar(255),
  `description` varchar(1024),
  `data_url` varchar(50),
  `meas_time` varchar(50),
  `date` datetime,
  `status` tinyint(4) NOT NULL DEFAULT '1',
  PRIMARY KEY(`id_online_data_id`),
  INDEX `FKIndex4`(`install_id`),
  CONSTRAINT `(install_id=install_id)` FOREIGN KEY (`install_id`)
    REFERENCES `install`(`install_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table install_rel_prop
DROP TABLE IF EXISTS `install_rel_prop`;

CREATE TABLE `install_rel_prop` (
  `install_rel__prop_id` int(11) NOT NULL AUTO_INCREMENT,
  `install_rel_id` int(11),
  `install_rel_prop_type_id` int(11),
  `install_rel_prop_value` varchar(255),
  PRIMARY KEY(`install_rel__prop_id`),
  INDEX `FKIndex1`(`install_rel_id`),
  INDEX `FKIndex2`(`install_rel_prop_type_id`),
  CONSTRAINT `(install_rel_id=install_rel_id)` FOREIGN KEY (`install_rel_id`)
    REFERENCES `install_rel`(`install_rel_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `(installl_rel_prop_type_id=installl_rel_prop_type_id)` FOREIGN KEY (`install_rel_prop_type_id`)
    REFERENCES `install_rel_prop_type`(`install_rel_prop_type_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table inventory__install
DROP TABLE IF EXISTS `inventory__install`;

CREATE TABLE `inventory__install` (
  `inventory__install_id` int(11) NOT NULL AUTO_INCREMENT,
  `install_id` int(11) NOT NULL DEFAULT '0',
  `inventory_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY(`inventory__install_id`),
  INDEX `FKIndex1`(`install_id`),
  INDEX `FKIndex2`(`inventory_id`),
  CONSTRAINT `(install_id= install_id)` FOREIGN KEY (`install_id`)
    REFERENCES `install`(`install_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `(inventory_id= inventory_id)` FOREIGN KEY (`inventory_id`)
    REFERENCES `inventory`(`inventory_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

SET FOREIGN_KEY_CHECKS=1;
