-- =============================================================================
-- Diagram Name: v0_5
-- Created on: 11/15/2013 11:40:49 AM
-- Diagram Version: 511
-- =============================================================================
SET FOREIGN_KEY_CHECKS=0;

-- Drop table active_interlock_prop_type
DROP TABLE IF EXISTS `active_interlock_prop_type`;

CREATE TABLE `active_interlock_prop_type` (
  `active_interlock_prop_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(127),
  `description` varchar(255),
  `unit` varchar(50),
  `created_date` datetime,
  PRIMARY KEY(`active_interlock_prop_type_id`),
  UNIQUE INDEX `name_unit`(`name`, `unit`)
)
ENGINE=INNODB;

-- Drop table active_interlock_logic
DROP TABLE IF EXISTS `active_interlock_logic`;

CREATE TABLE `active_interlock_logic` (
  `active_interlock_logic_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50),
  `shape` varchar(50),
  `logic` varchar(255),
  `logic_code` int(11),
  `status` int(11),
  `created_by` varchar(50),
  `created_date` datetime,
  PRIMARY KEY(`active_interlock_logic_id`),
  UNIQUE INDEX `name`(`name`)
)
ENGINE=INNODB;

-- Drop table active_interlock
DROP TABLE IF EXISTS `active_interlock`;

CREATE TABLE `active_interlock` (
  `active_interlock_id` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(255),
  `status` int(11),
  `rawdata` mediumtext,
  `created_by` varchar(50),
  `created_date` datetime,
  `modified_by` varchar(50),
  `modified_date` datetime,
  PRIMARY KEY(`active_interlock_id`)
)
ENGINE=INNODB;

-- Drop table active_interlock_device
DROP TABLE IF EXISTS `active_interlock_device`;

CREATE TABLE `active_interlock_device` (
  `active_interlock_device_id` int(11) NOT NULL AUTO_INCREMENT,
  `active_interlock_id` int(11) NOT NULL DEFAULT '0',
  `active_interlock_logic_id` int(11),
  `device_name` varchar(50),
  `definition` varchar(255),
  PRIMARY KEY(`active_interlock_device_id`),
  CONSTRAINT `Ref_07` FOREIGN KEY (`active_interlock_id`)
    REFERENCES `active_interlock`(`active_interlock_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_13` FOREIGN KEY (`active_interlock_logic_id`)
    REFERENCES `active_interlock_logic`(`active_interlock_logic_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table active_interlock_prop
DROP TABLE IF EXISTS `active_interlock_prop`;

CREATE TABLE `active_interlock_prop` (
  `active_interlock_prop_id` int(11) NOT NULL AUTO_INCREMENT,
  `active_interlock_device_id` int(11),
  `active_interlock_prop_type_id` int(11),
  `value` varchar(1024),
  `status` tinyint(4),
  `date` datetime,
  PRIMARY KEY(`active_interlock_prop_id`),
  CONSTRAINT `Ref_05` FOREIGN KEY (`active_interlock_device_id`)
    REFERENCES `active_interlock_device`(`active_interlock_device_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_06` FOREIGN KEY (`active_interlock_prop_type_id`)
    REFERENCES `active_interlock_prop_type`(`active_interlock_prop_type_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

SET FOREIGN_KEY_CHECKS=1;
