-- =============================================================================
-- Diagram Name: v0_6
-- Created on: 8/26/2014 9:57:25 AM
-- Diagram Version: 534
-- =============================================================================
SET FOREIGN_KEY_CHECKS=0;

-- Drop table beamline_sequence
DROP TABLE IF EXISTS `beamline_sequence`;

CREATE TABLE `beamline_sequence` (
  `beamline_sequence_id` int(11) NOT NULL AUTO_INCREMENT,
  `sequence_name` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `first_element_name` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `last_element_name` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `previous_section` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `sequence_length` double,
  `sequence_description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci,
  PRIMARY KEY(`beamline_sequence_id`)
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

-- Drop table machine_mode
DROP TABLE IF EXISTS `machine_mode`;

CREATE TABLE `machine_mode` (
  `machine_mode_id` int(11) NOT NULL AUTO_INCREMENT,
  `machine_mode_name` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `machine_mode_description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci,
  PRIMARY KEY(`machine_mode_id`)
)
ENGINE=INNODB;

-- Drop table cmpnt_type_prop_type
DROP TABLE IF EXISTS `cmpnt_type_prop_type`;

CREATE TABLE `cmpnt_type_prop_type` (
  `cmpnt_type_prop_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `cmpnt_type_prop_type_name` varchar(255),
  `cmpnt_type_prop_type_desc` varchar(255),
  PRIMARY KEY(`cmpnt_type_prop_type_id`)
)
ENGINE=INNODB;

-- Drop table model_geometry
DROP TABLE IF EXISTS `model_geometry`;

CREATE TABLE `model_geometry` (
  `model_geometry_id` int(11) NOT NULL AUTO_INCREMENT,
  `model_geometry_name` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `model_geometry_description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci,
  PRIMARY KEY(`model_geometry_id`)
)
ENGINE=INNODB;

-- Drop table model_code
DROP TABLE IF EXISTS `model_code`;

CREATE TABLE `model_code` (
  `model_code_id` int(11) NOT NULL AUTO_INCREMENT,
  `code_name` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `algorithm` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci,
  PRIMARY KEY(`model_code_id`),
  UNIQUE INDEX `code_name_algorithm`(`code_name`, `algorithm`)
)
ENGINE=INNODB;

-- Drop table element_type
DROP TABLE IF EXISTS `element_type`;

CREATE TABLE `element_type` (
  `element_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `element_type_name` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `element_type_description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci,
  PRIMARY KEY(`element_type_id`),
  UNIQUE INDEX `element_type_name`(`element_type_name`)
)
ENGINE=INNODB;

-- Drop table model_line
DROP TABLE IF EXISTS `model_line`;

CREATE TABLE `model_line` (
  `model_line_id` int(11) NOT NULL AUTO_INCREMENT,
  `model_line_name` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `model_line_description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `start_position` double,
  `end_position` double,
  `start_marker` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `end_marker` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci,
  PRIMARY KEY(`model_line_id`)
)
ENGINE=INNODB;

-- Drop table vendor
DROP TABLE IF EXISTS `vendor`;

CREATE TABLE `vendor` (
  `vendor_id` int(11) NOT NULL AUTO_INCREMENT,
  `vendor_name` varchar(100) NOT NULL,
  `vendor_description` varchar(255),
  PRIMARY KEY(`vendor_id`)
)
ENGINE=INNODB;

-- Drop table cmpnt_type
DROP TABLE IF EXISTS `cmpnt_type`;

CREATE TABLE `cmpnt_type` (
  `cmpnt_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `cmpnt_type_name` varchar(100) NOT NULL,
  `description` text,
  PRIMARY KEY(`cmpnt_type_id`),
  UNIQUE INDEX `idx_cmpnt_type_name_unique`(`cmpnt_type_name`)
)
ENGINE=INNODB;

-- Drop table id_raw_data
DROP TABLE IF EXISTS `id_raw_data`;

CREATE TABLE `id_raw_data` (
  `id_raw_data_id` int(11) NOT NULL AUTO_INCREMENT,
  `data` mediumblob,
  PRIMARY KEY(`id_raw_data_id`)
)
ENGINE=INNODB;

-- Drop table id_data_method
DROP TABLE IF EXISTS `id_data_method`;

CREATE TABLE `id_data_method` (
  `id_data_method_id` int(11) NOT NULL AUTO_INCREMENT,
  `method_name` varchar(255),
  `description` varchar(255),
  PRIMARY KEY(`id_data_method_id`)
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

-- Drop table lattice_type
DROP TABLE IF EXISTS `lattice_type`;

CREATE TABLE `lattice_type` (
  `lattice_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `lattice_type_name` varchar(255),
  `lattice_type_format` varchar(10),
  PRIMARY KEY(`lattice_type_id`),
  UNIQUE INDEX `name_format`(`lattice_type_name`, `lattice_type_format`)
)
ENGINE=INNODB;

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

-- Drop table element_type_prop
DROP TABLE IF EXISTS `element_type_prop`;

CREATE TABLE `element_type_prop` (
  `element_type_prop_id` int(11) NOT NULL AUTO_INCREMENT,
  `element_type_id` int(11),
  `element_type_prop_name` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `element_type_prop_description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `element_type_prop_default` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `element_type_prop_unit` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci,
  PRIMARY KEY(`element_type_prop_id`),
  CONSTRAINT `Ref_230` FOREIGN KEY (`element_type_id`)
    REFERENCES `element_type`(`element_type_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table inventory_prop_tmplt
DROP TABLE IF EXISTS `inventory_prop_tmplt`;

CREATE TABLE `inventory_prop_tmplt` (
  `inventory_prop_tmplt_id` int(11) NOT NULL AUTO_INCREMENT,
  `cmpnt_type_id` int(11) NOT NULL DEFAULT '0',
  `inventory_prop_tmplt_name` varchar(50),
  `inventory_prop_tmplt_desc` varchar(255),
  `inventory_prop_tmplt_default` varchar(255),
  `inventory_prop_tmplt_units` varchar(50),
  PRIMARY KEY(`inventory_prop_tmplt_id`),
  CONSTRAINT `Ref_169` FOREIGN KEY (`cmpnt_type_id`)
    REFERENCES `cmpnt_type`(`cmpnt_type_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table install
DROP TABLE IF EXISTS `install`;

CREATE TABLE `install` (
  `install_id` int(11) NOT NULL AUTO_INCREMENT,
  `cmpnt_type_id` int(11) NOT NULL DEFAULT '0',
  `field_name` varchar(255),
  `location` varchar(255),
  `coordinate_center` float,
  PRIMARY KEY(`install_id`),
  UNIQUE INDEX `field_name`(`field_name`),
  CONSTRAINT `Ref_99` FOREIGN KEY (`cmpnt_type_id`)
    REFERENCES `cmpnt_type`(`cmpnt_type_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
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
  `location` varchar(255),
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

-- Drop table inventory
DROP TABLE IF EXISTS `inventory`;

CREATE TABLE `inventory` (
  `inventory_id` int(11) NOT NULL AUTO_INCREMENT,
  `cmpnt_type_id` int(11) NOT NULL,
  `vendor_id` int(11),
  `name` varchar(100),
  `alias` varchar(100),
  `serial_no` varchar(255),
  PRIMARY KEY(`inventory_id`),
  INDEX `idx_cmpnt_type_id_c`(`cmpnt_type_id`),
  UNIQUE INDEX `new_index64`(`name`),
  CONSTRAINT `cmpnt_ibfk_1` FOREIGN KEY (`cmpnt_type_id`)
    REFERENCES `cmpnt_type`(`cmpnt_type_id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `Ref_244` FOREIGN KEY (`vendor_id`)
    REFERENCES `vendor`(`vendor_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table activeinterlocldevice__install
DROP TABLE IF EXISTS `activeinterlocldevice__install`;

CREATE TABLE `activeinterlocldevice__install` (
  `activeinterlocldevice__install_id` int(11) NOT NULL AUTO_INCREMENT,
  `active_interlock_device_id` int(11),
  `install_id` int(11),
  PRIMARY KEY(`activeinterlocldevice__install_id`),
  CONSTRAINT `Ref_02` FOREIGN KEY (`active_interlock_device_id`)
    REFERENCES `active_interlock_device`(`active_interlock_device_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_03` FOREIGN KEY (`install_id`)
    REFERENCES `install`(`install_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table install_rel
DROP TABLE IF EXISTS `install_rel`;

CREATE TABLE `install_rel` (
  `install_rel_id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_install_id` int(11) NOT NULL DEFAULT '0',
  `child_install_id` int(11) NOT NULL DEFAULT '0',
  `logical_desc` varchar(60),
  `logical_order` int(11),
  `install_date` datetime,
  PRIMARY KEY(`install_rel_id`),
  CONSTRAINT `Ref_100` FOREIGN KEY (`parent_install_id`)
    REFERENCES `install`(`install_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_101` FOREIGN KEY (`child_install_id`)
    REFERENCES `install`(`install_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table cmpnt_type_prop
DROP TABLE IF EXISTS `cmpnt_type_prop`;

CREATE TABLE `cmpnt_type_prop` (
  `cmpnt_type_prop_id` int(11) NOT NULL AUTO_INCREMENT,
  `cmpnt_type_id` int(11) NOT NULL DEFAULT '0',
  `cmpnt_type_prop_type_id` int(11),
  `cmpnt_type_prop_value` varchar(4096),
  PRIMARY KEY(`cmpnt_type_prop_id`),
  CONSTRAINT `Ref_188` FOREIGN KEY (`cmpnt_type_prop_type_id`)
    REFERENCES `cmpnt_type_prop_type`(`cmpnt_type_prop_type_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_189` FOREIGN KEY (`cmpnt_type_id`)
    REFERENCES `cmpnt_type`(`cmpnt_type_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table cmpnttype__vendor
DROP TABLE IF EXISTS `cmpnttype__vendor`;

CREATE TABLE `cmpnttype__vendor` (
  `cmpnttype__vendor_id` int(11) NOT NULL AUTO_INCREMENT,
  `vendor_id` int(11),
  `cmpnt_type_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY(`cmpnttype__vendor_id`),
  CONSTRAINT `Ref_236` FOREIGN KEY (`vendor_id`)
    REFERENCES `vendor`(`vendor_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_242` FOREIGN KEY (`cmpnt_type_id`)
    REFERENCES `cmpnt_type`(`cmpnt_type_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table id_offline_data
DROP TABLE IF EXISTS `id_offline_data`;

CREATE TABLE `id_offline_data` (
  `id_offline_data_id` int(11) NOT NULL AUTO_INCREMENT,
  `inventory_id` int(11) NOT NULL,
  `id_data_method_id` int(11),
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
  `script_file_content` mediumblob,
  PRIMARY KEY(`id_offline_data_id`),
  INDEX `FKIndex1`(`id_data_method_id`),
  INDEX `FKIndex2`(`inventory_id`),
  INDEX `FKIndex3`(`id_raw_data_id`),
  CONSTRAINT `Ref_15` FOREIGN KEY (`id_raw_data_id`)
    REFERENCES `id_raw_data`(`id_raw_data_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_19` FOREIGN KEY (`id_data_method_id`)
    REFERENCES `id_data_method`(`id_data_method_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_20` FOREIGN KEY (`inventory_id`)
    REFERENCES `inventory`(`inventory_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB
CHARACTER SET latin1 
COLLATE latin1_swedish_ci ;

-- Drop table lattice
DROP TABLE IF EXISTS `lattice`;

CREATE TABLE `lattice` (
  `lattice_id` int(11) NOT NULL AUTO_INCREMENT,
  `lattice_type_id` int(11),
  `model_line_id` int(11),
  `machine_mode_id` int(11),
  `model_geometry_id` int(11),
  `lattice_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `lattice_version` int(50),
  `lattice_branch` varchar(50),
  `lattice_description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `created_by` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `create_date` datetime,
  `updated_by` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `update_date` datetime,
  `url` varchar(255),
  PRIMARY KEY(`lattice_id`),
  UNIQUE INDEX `lattice_name_version_branch`(`lattice_name`, `lattice_version`, `lattice_branch`),
  CONSTRAINT `FK_model_line` FOREIGN KEY (`model_line_id`)
    REFERENCES `model_line`(`model_line_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_model_geometry` FOREIGN KEY (`model_geometry_id`)
    REFERENCES `model_geometry`(`model_geometry_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_machine_mode` FOREIGN KEY (`machine_mode_id`)
    REFERENCES `machine_mode`(`machine_mode_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_01` FOREIGN KEY (`lattice_type_id`)
    REFERENCES `lattice_type`(`lattice_type_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table gold_lattice
DROP TABLE IF EXISTS `gold_lattice`;

CREATE TABLE `gold_lattice` (
  `gold_lattice_id` int(11) NOT NULL AUTO_INCREMENT,
  `lattice_id` int(11),
  `created_by` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `create_date` datetime,
  `updated_by` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `update_date` datetime,
  `gold_status_ind` int(11),
  PRIMARY KEY(`gold_lattice_id`),
  CONSTRAINT `FK_gold_lattice_id` FOREIGN KEY (`lattice_id`)
    REFERENCES `lattice`(`lattice_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table id_online_data
DROP TABLE IF EXISTS `id_online_data`;

CREATE TABLE `id_online_data` (
  `id_online_data_id` int(11) NOT NULL AUTO_INCREMENT,
  `install_id` int(11) NOT NULL DEFAULT '0',
  `login_name` varchar(255),
  `description` varchar(1024),
  `rawdata_path` varchar(255),
  `feedforward_file_name` varchar(255),
  `feedforward_data` mediumblob,
  `meas_time` varchar(50),
  `date` datetime,
  `status` tinyint(4) NOT NULL DEFAULT '1',
  PRIMARY KEY(`id_online_data_id`),
  INDEX `FKIndex4`(`install_id`),
  CONSTRAINT `Ref_14` FOREIGN KEY (`install_id`)
    REFERENCES `install`(`install_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table hall_probe_data
DROP TABLE IF EXISTS `hall_probe_data`;

CREATE TABLE `hall_probe_data` (
  `hall_probe_id` int(11) NOT NULL AUTO_INCREMENT,
  `inventory_id` int(11),
  `alias` varchar(50),
  `meas_date` datetime,
  `measured_at_location` varchar(50),
  `sub_device` varchar(50) NOT NULL DEFAULT '0',
  `run_identifier` varchar(50),
  `login_name` varchar(50),
  `conditioning_current` double,
  `current_1` double,
  `current_2` double,
  `current_3` double,
  `up_dn1` varchar(50),
  `up_dn2` varchar(50),
  `up_dn3` varchar(50),
  `mag_volt_1` double,
  `mag_volt_2` double,
  `mag_volt_3` double,
  `x` double,
  `y` double,
  `z` double,
  `bx_t` double,
  `by_t` double,
  `bz_t` double,
  `meas_notes` varchar(255),
  `data_issues` varchar(255),
  `data_usage` int(11),
  PRIMARY KEY(`hall_probe_id`),
  CONSTRAINT `Ref_165` FOREIGN KEY (`inventory_id`)
    REFERENCES `inventory`(`inventory_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table rot_coil_data
DROP TABLE IF EXISTS `rot_coil_data`;

CREATE TABLE `rot_coil_data` (
  `rot_coil_data_id` int(11) NOT NULL AUTO_INCREMENT,
  `inventory_id` int(11) NOT NULL DEFAULT '0',
  `alias` varchar(50),
  `meas_coil_id` varchar(50),
  `ref_radius` double,
  `magnet_notes` varchar(50),
  `login_name` varchar(2000),
  `cond_curr` double,
  `meas_loc` varchar(50),
  `run_number` varchar(50),
  `sub_device` varchar(50),
  `current_1` double,
  `current_2` double,
  `current_3` double,
  `up_dn_1` varchar(50),
  `up_dn_2` varchar(50),
  `up_dn_3` varchar(50),
  `analysis_number` varchar(50),
  `integral_xfer_function` double,
  `orig_offset_x` double,
  `orig_offset_y` double,
  `B_ref_int` double,
  `Roll_angle` double,
  `meas_notes` varchar(2000),
  `meas_date` datetime,
  `author` varchar(50),
  `a1` double,
  `a2` double,
  `a3` double,
  `b1` double,
  `b2` double,
  `b3` double,
  `a4_21` varchar(255),
  `b4_21` varchar(255),
  `data_issues` varchar(50),
  `data_usage` int(11),
  PRIMARY KEY(`rot_coil_data_id`),
  CONSTRAINT `Ref_192` FOREIGN KEY (`inventory_id`)
    REFERENCES `inventory`(`inventory_id`)
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

-- Drop table install_rel_prop
DROP TABLE IF EXISTS `install_rel_prop`;

CREATE TABLE `install_rel_prop` (
  `install_rel__prop_id` int(11) NOT NULL AUTO_INCREMENT,
  `install_rel_id` int(11),
  `install_rel_prop_type_id` int(11),
  `install_rel_prop_value` varchar(255),
  PRIMARY KEY(`install_rel__prop_id`),
  CONSTRAINT `Ref_184` FOREIGN KEY (`install_rel_id`)
    REFERENCES `install_rel`(`install_rel_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_208` FOREIGN KEY (`install_rel_prop_type_id`)
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
  CONSTRAINT `Ref_104` FOREIGN KEY (`install_id`)
    REFERENCES `install`(`install_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_102` FOREIGN KEY (`inventory_id`)
    REFERENCES `inventory`(`inventory_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table inventory_prop
DROP TABLE IF EXISTS `inventory_prop`;

CREATE TABLE `inventory_prop` (
  `inventory_prop_id` int(11) NOT NULL AUTO_INCREMENT,
  `inventory_id` int(11) NOT NULL,
  `inventory_prop_tmplt_id` int(11) NOT NULL DEFAULT '0',
  `inventory_prop_value` varchar(4096),
  PRIMARY KEY(`inventory_prop_id`),
  INDEX `idx_cmpnt_id`(`inventory_id`),
  CONSTRAINT `Ref_71` FOREIGN KEY (`inventory_id`)
    REFERENCES `inventory`(`inventory_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_172` FOREIGN KEY (`inventory_prop_tmplt_id`)
    REFERENCES `inventory_prop_tmplt`(`inventory_prop_tmplt_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table element
DROP TABLE IF EXISTS `element`;

CREATE TABLE `element` (
  `element_id` int(11) NOT NULL AUTO_INCREMENT,
  `lattice_id` int(11),
  `element_type_id` int(11),
  `element_name` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `element_order` int(11),
  `insert_date` datetime,
  `created_by` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `s` double,
  `length` double,
  `dx` double,
  `dy` double,
  `dz` double,
  `pitch` double,
  `yaw` double,
  `roll` double,
  PRIMARY KEY(`element_id`),
  CONSTRAINT `FK_lattice_element` FOREIGN KEY (`lattice_id`)
    REFERENCES `lattice`(`lattice_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_element_type` FOREIGN KEY (`element_type_id`)
    REFERENCES `element_type`(`element_type_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table blsequence__lattice
DROP TABLE IF EXISTS `blsequence__lattice`;

CREATE TABLE `blsequence__lattice` (
  `blsequence__lattice_id` int(11) NOT NULL AUTO_INCREMENT,
  `beamline_sequence_id` int(11),
  `lattice_id` int(11),
  `beamline_order` int(11),
  PRIMARY KEY(`blsequence__lattice_id`),
  CONSTRAINT `Ref_18` FOREIGN KEY (`beamline_sequence_id`)
    REFERENCES `beamline_sequence`(`beamline_sequence_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_16` FOREIGN KEY (`lattice_id`)
    REFERENCES `lattice`(`lattice_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table model
DROP TABLE IF EXISTS `model`;

CREATE TABLE `model` (
  `model_id` int(11) NOT NULL AUTO_INCREMENT,
  `lattice_id` int(11),
  `model_code_id` int(11),
  `model_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `model_desc` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `created_by` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `create_date` datetime,
  `updated_by` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `update_date` datetime,
  `tune_x` double,
  `tune_y` double,
  `alphac` double,
  `alphac2` double,
  `chrome_x_0` double,
  `chrome_x_1` double,
  `chrome_x_2` double,
  `chrome_y_0` double,
  `chrome_y_1` double,
  `chrome_y_2` double,
  `final_beam_energy` double,
  `model_control_data` mediumtext,
  `model_control_name` varchar(255),
  PRIMARY KEY(`model_id`),
  UNIQUE INDEX `model_name`(`model_name`),
  CONSTRAINT `FK_model_code` FOREIGN KEY (`model_code_id`)
    REFERENCES `model_code`(`model_code_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_lattice` FOREIGN KEY (`lattice_id`)
    REFERENCES `lattice`(`lattice_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table element_prop
DROP TABLE IF EXISTS `element_prop`;

CREATE TABLE `element_prop` (
  `element_prop_id` int(11) NOT NULL AUTO_INCREMENT,
  `element_id` int(11),
  `element_type_prop_id` int(11),
  `element_prop_value` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `element_prop_unit` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `element_prop_index` int(11),
  PRIMARY KEY(`element_prop_id`),
  CONSTRAINT `Ref_17` FOREIGN KEY (`element_type_prop_id`)
    REFERENCES `element_type_prop`(`element_type_prop_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_element_id` FOREIGN KEY (`element_id`)
    REFERENCES `element`(`element_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table gold_model
DROP TABLE IF EXISTS `gold_model`;

CREATE TABLE `gold_model` (
  `gold_model_id` int(11) NOT NULL AUTO_INCREMENT,
  `model_id` int(11),
  `created_by` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `create_date` datetime,
  `updated_by` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `update_date` datetime,
  `gold_status_ind` int(11),
  PRIMARY KEY(`gold_model_id`),
  CONSTRAINT `Ref_215` FOREIGN KEY (`model_id`)
    REFERENCES `model`(`model_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table beam_parameter
DROP TABLE IF EXISTS `beam_parameter`;

CREATE TABLE `beam_parameter` (
  `beam_parameter_id` int(11) NOT NULL AUTO_INCREMENT,
  `element_id` int(11),
  `model_id` int(11),
  `pos` double,
  `alpha_x` double,
  `beta_x` double,
  `nu_x` double,
  `eta_x` double,
  `etap_x` double,
  `alpha_y` double,
  `beta_y` double,
  `nu_y` double,
  `eta_y` double,
  `etap_y` double,
  `transfer_matrix` varchar(2047) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `co_x` double,
  `co_y` double,
  `index_slice_chk` int(11),
  `s` double,
  `energy` double,
  `particle_species` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `particle_mass` double,
  `particle_charge` int(11),
  `beam_charge_density` double,
  `beam_current` double,
  `x` double,
  `xp` double,
  `y` double,
  `yp` double,
  `z` double,
  `zp` double,
  `emit_x` double,
  `emit_y` double,
  `emit_z` double,
  PRIMARY KEY(`beam_parameter_id`),
  CONSTRAINT `FK_element` FOREIGN KEY (`element_id`)
    REFERENCES `element`(`element_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_212` FOREIGN KEY (`model_id`)
    REFERENCES `model`(`model_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table element__install
DROP TABLE IF EXISTS `element__install`;

CREATE TABLE `element__install` (
  `element__install_id` int(11) NOT NULL,
  `element_id` int(11),
  `install_id` int(11),
  `slice` int(11),
  `index` int(11),
  PRIMARY KEY(`element__install_id`),
  CONSTRAINT `FK_element_install` FOREIGN KEY (`element_id`)
    REFERENCES `element`(`element_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_216` FOREIGN KEY (`install_id`)
    REFERENCES `install`(`install_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

SET FOREIGN_KEY_CHECKS=1;
