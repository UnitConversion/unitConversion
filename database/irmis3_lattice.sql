-- =============================================================================
-- Diagram Name: v0_5
-- Created on: 4/4/2013 10:18:54 AM
-- Diagram Version: 472
-- =============================================================================
SET FOREIGN_KEY_CHECKS=0;

-- Drop table machine_mode
DROP TABLE IF EXISTS `machine_mode`;

CREATE TABLE `machine_mode` (
  `machine_mode_id` int(11) NOT NULL AUTO_INCREMENT,
  `machine_mode_name` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `machine_mode_description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci,
  PRIMARY KEY(`machine_mode_id`)
)
ENGINE=INNODB;

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

-- Drop table element_type
DROP TABLE IF EXISTS `element_type`;

CREATE TABLE `element_type` (
  `element_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `element_type_name` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `element_type_description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci,
  PRIMARY KEY(`element_type_id`)
)
ENGINE=INNODB;

-- Drop table model_code
DROP TABLE IF EXISTS `model_code`;

CREATE TABLE `model_code` (
  `model_code_id` int(11) NOT NULL AUTO_INCREMENT,
  `code_name` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `algorithm` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `config_file_content` mediumtext,
  `config_file_name` varchar(255),
  PRIMARY KEY(`model_code_id`)
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

-- Drop table lattice_type
DROP TABLE IF EXISTS `lattice_type`;

CREATE TABLE `lattice_type` (
  `lattice_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `lattice_type_name` varchar(255),
  `lattice_type_format` varchar(10),
  PRIMARY KEY(`lattice_type_id`)
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

-- Drop table element_type_prop
DROP TABLE IF EXISTS `element_type_prop`;

CREATE TABLE `element_type_prop` (
  `element_type_prop_id` int(11) NOT NULL AUTO_INCREMENT,
  `element_type_id` int(11),
  `element_type_prop_name` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `element_type_prop_description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `element_type_prop_default` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `element_type_prop_unit` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `element_type_prop_datatype` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci,
  PRIMARY KEY(`element_type_prop_id`),
  CONSTRAINT `Ref_230` FOREIGN KEY (`element_type_id`)
    REFERENCES `element_type`(`element_type_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

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
  `chrome_x_0` double,
  `chrome_x_1` double,
  `chrome_x_2` double,
  `chrome_y_0` double,
  `chrome_y_1` double,
  `chrome_y_2` double,
  `final_beam_energy` double,
  PRIMARY KEY(`model_id`),
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
  `twiss_id` int(11) NOT NULL AUTO_INCREMENT,
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
  `particel_species` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `particle mass` double,
  `particle charge` int(11),
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
  PRIMARY KEY(`twiss_id`),
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

-- Drop table element_prop
DROP TABLE IF EXISTS `element_prop`;

CREATE TABLE `element_prop` (
  `element_prop_id` int(11) NOT NULL AUTO_INCREMENT,
  `element_id` int(11),
  `element_type_prop_id` int(11),
  `element_prop_string` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `element_prop_int` int(11),
  `element_prop_double` double,
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

SET FOREIGN_KEY_CHECKS=1;
