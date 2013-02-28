-- =============================================================================
-- Diagram Name: v0_2
-- Created on: 12/11/2012 5:04:47 PM
-- Diagram Version: 337
-- =============================================================================
SET FOREIGN_KEY_CHECKS=0;

-- Drop table service
DROP TABLE IF EXISTS `service`;

CREATE TABLE `service` (
  `service_id` int(11) NOT NULL AUTO_INCREMENT,
  `service_name` varchar(50),
  `service_desc` varchar(255),
  PRIMARY KEY(`service_id`)
)
ENGINE=INNODB;

-- Drop table ioc_status
DROP TABLE IF EXISTS `ioc_status`;

CREATE TABLE `ioc_status` (
  `ioc_status_id` int(11) NOT NULL AUTO_INCREMENT,
  `ioc_status` varchar(50),
  PRIMARY KEY(`ioc_status_id`)
)
ENGINE=INNODB;

-- Drop table pv
DROP TABLE IF EXISTS `pv`;

CREATE TABLE `pv` (
  `pv_id` int(11) NOT NULL AUTO_INCREMENT,
  `pv_name` varchar(128) NOT NULL,
  `description` text,
  PRIMARY KEY(`pv_id`),
  INDEX `idx_pv_name`(`pv_name`)
)
ENGINE=INNODB;

-- Drop table pgroup
DROP TABLE IF EXISTS `pgroup`;

CREATE TABLE `pgroup` (
  `pgroup_id` int(11) NOT NULL AUTO_INCREMENT,
  `pgroup_name` int(11),
  PRIMARY KEY(`pgroup_id`)
)
ENGINE=INNODB;

-- Drop table pv_group
DROP TABLE IF EXISTS `pv_group`;

CREATE TABLE `pv_group` (
  `pv_group_id` int(11) NOT NULL AUTO_INCREMENT,
  `pv_group_name` varchar(50),
  `pv_group_func` varchar(50),
  `pvg_creation_date` timestamp DEFAULT current_timestamp,
  `version` varchar(50),
  PRIMARY KEY(`pv_group_id`)
)
ENGINE=INNODB;

-- Drop table rec_client_type
DROP TABLE IF EXISTS `rec_client_type`;

CREATE TABLE `rec_client_type` (
  `rec_client_type_id` int(11) NOT NULL,
  `description` varchar(100),
  PRIMARY KEY(`rec_client_type_id`)
)
ENGINE=INNODB;

-- Drop table port_type
DROP TABLE IF EXISTS `port_type`;

CREATE TABLE `port_type` (
  `port_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `connector_type` varchar(60) NOT NULL,
  `connector_group` varchar(60) NOT NULL,
  `pin_count` int(11),
  PRIMARY KEY(`port_type_id`),
  UNIQUE INDEX `idx_port_type_group_unique`(`connector_type`, `connector_group`)
)
ENGINE=INNODB;

-- Drop table ioc_proptype
DROP TABLE IF EXISTS `ioc_proptype`;

CREATE TABLE `ioc_proptype` (
  `ioc_proptype_id` int(11) NOT NULL AUTO_INCREMENT,
  `ioc_proptype_name` varchar(50),
  `ioc_proptype_desc` varchar(50),
  PRIMARY KEY(`ioc_proptype_id`)
)
ENGINE=INNODB;

-- Drop table uri
DROP TABLE IF EXISTS `uri`;

CREATE TABLE `uri` (
  `uri_id` int(11) NOT NULL AUTO_INCREMENT,
  `uri` varchar(255),
  `uri_modified_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `modified_by` varchar(10),
  PRIMARY KEY(`uri_id`)
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

-- Drop table person
DROP TABLE IF EXISTS `person`;

CREATE TABLE `person` (
  `person_id` int(11) NOT NULL AUTO_INCREMENT,
  `last_name` varchar(50) NOT NULL DEFAULT '0',
  `first_name` varchar(50),
  `telephone` varchar(50),
  `email` varchar(50),
  `bldg` varchar(50),
  `room` varchar(50),
  `life_no` int(11),
  PRIMARY KEY(`person_id`)
)
ENGINE=INNODB;

-- Drop table elog_tag
DROP TABLE IF EXISTS `elog_tag`;

CREATE TABLE `elog_tag` (
  `elog_tag_id` int(11) NOT NULL AUTO_INCREMENT,
  `elog_tag` char(50) NOT NULL,
  `description` varchar(255),
  PRIMARY KEY(`elog_tag_id`)
)
ENGINE=INNODB;

-- Drop table doc
DROP TABLE IF EXISTS `doc`;

CREATE TABLE `doc` (
  `doc_id` int(11) NOT NULL AUTO_INCREMENT,
  `doc type` varchar(50),
  `doc_url` varchar(50),
  PRIMARY KEY(`doc_id`)
)
ENGINE=INNODB;

-- Drop table pv_attrtype
DROP TABLE IF EXISTS `pv_attrtype`;

CREATE TABLE `pv_attrtype` (
  `pv_attrtype_id` int(11) NOT NULL AUTO_INCREMENT,
  `pv_attrtype_name` varchar(50),
  `pv_attrtype_desc` varchar(255),
  PRIMARY KEY(`pv_attrtype_id`)
)
ENGINE=INNODB;

-- Drop table elog_book
DROP TABLE IF EXISTS `elog_book`;

CREATE TABLE `elog_book` (
  `elog_book_id` int(11) NOT NULL,
  `elog_book_name` varchar(50),
  `elog_book_type` varchar(50),
  `elog_book_group` varchar(50),
  `elog_book_start_date` timestamp DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY(`elog_book_id`)
)
ENGINE=INNODB;

-- Drop table iocboot_proptype
DROP TABLE IF EXISTS `iocboot_proptype`;

CREATE TABLE `iocboot_proptype` (
  `iocboot_proptype_id` int(11) NOT NULL AUTO_INCREMENT,
  `iocboot_proptype_name` varchar(50),
  `iocboot_proptype_desc` varchar(255),
  PRIMARY KEY(`iocboot_proptype_id`)
)
ENGINE=INNODB;

-- Drop table role
DROP TABLE IF EXISTS `role`;

CREATE TABLE `role` (
  `role_id` int(11) NOT NULL AUTO_INCREMENT,
  `role` int(11),
  PRIMARY KEY(`role_id`)
)
ENGINE=INNODB;

-- Drop table cable_type
DROP TABLE IF EXISTS `cable_type`;

CREATE TABLE `cable_type` (
  `cable_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `cable_type` varchar(50),
  `cable_type_description` varchar(255),
  `cable_diameter` float,
  `ampacity` double,
  PRIMARY KEY(`cable_type_id`)
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

-- Drop table partition_type
DROP TABLE IF EXISTS `partition_type`;

CREATE TABLE `partition_type` (
  `partition_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `partition_type` varchar(50),
  `partition_type_description` varchar(255),
  PRIMARY KEY(`partition_type_id`)
)
ENGINE=INNODB;

-- Drop table workflow_tmplt
DROP TABLE IF EXISTS `workflow_tmplt`;

CREATE TABLE `workflow_tmplt` (
  `workflow_tmplt_id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(50),
  `workflow_description` varchar(255),
  `revision` varchar(50),
  `revision_date` datetime,
  `requires_inventory` enum('none','one','one or more','zero or more','zero or one'),
  `recurring_period_number` int(11),
  `recurring_period_unit` varchar(50),
  `workflow_type` varchar(50),
  PRIMARY KEY(`workflow_tmplt_id`)
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

-- Drop table irmis_version
DROP TABLE IF EXISTS `irmis_version`;

CREATE TABLE `irmis_version` (
  `irmis_version_id` int(11) NOT NULL AUTO_INCREMENT,
  `irmis_version` varchar(50),
  `description` text,
  `irmis_version_date` datetime,
  PRIMARY KEY(`irmis_version_id`)
)
ENGINE=INNODB;

-- Drop table machine_mode
DROP TABLE IF EXISTS `machine_mode`;

CREATE TABLE `machine_mode` (
  `machine_mode_id` int(11) NOT NULL AUTO_INCREMENT,
  `machine_mode_name` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `machine_mode_description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci,
  PRIMARY KEY(`machine_mode_id`)
)
ENGINE=INNODB;

-- Drop table bundle_pull
DROP TABLE IF EXISTS `bundle_pull`;

CREATE TABLE `bundle_pull` (
  `bundle_pull_id` int(11) NOT NULL AUTO_INCREMENT,
  `bundle_label` varchar(255),
  `bundle_identifier` varchar(50),
  `cable_count` int(11) DEFAULT '1',
  `owner` varchar(50) DEFAULT 'unknown',
  `install_check` int(11),
  PRIMARY KEY(`bundle_pull_id`)
)
ENGINE=INNODB;

-- Drop table signal_type
DROP TABLE IF EXISTS `signal_type`;

CREATE TABLE `signal_type` (
  `signal_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `signal_type` varchar(50),
  PRIMARY KEY(`signal_type_id`)
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

-- Drop table install_rel_type
DROP TABLE IF EXISTS `install_rel_type`;

CREATE TABLE `install_rel_type` (
  `install_rel_type_id` int(11) NOT NULL,
  `rel_name` varchar(30),
  PRIMARY KEY(`install_rel_type_id`)
)
ENGINE=INNODB;

-- Drop table element_type
DROP TABLE IF EXISTS `element_type`;

CREATE TABLE `element_type` (
  `element_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `element_type` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `element_type_description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci,
  PRIMARY KEY(`element_type_id`)
)
ENGINE=INNODB;

-- Drop table signal_quality
DROP TABLE IF EXISTS `signal_quality`;

CREATE TABLE `signal_quality` (
  `signal_quality_id` int(11) NOT NULL AUTO_INCREMENT,
  `signal_quality` varchar(50),
  PRIMARY KEY(`signal_quality_id`)
)
ENGINE=INNODB;

-- Drop table model_code
DROP TABLE IF EXISTS `model_code`;

CREATE TABLE `model_code` (
  `model_code_id` int(11) NOT NULL AUTO_INCREMENT,
  `code_name` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `algorithm` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci,
  PRIMARY KEY(`model_code_id`)
)
ENGINE=INNODB;

-- Drop table ioc_resource_type
DROP TABLE IF EXISTS `ioc_resource_type`;

CREATE TABLE `ioc_resource_type` (
  `ioc_resource_type_id` int(11) NOT NULL,
  `ioc_resource_type` varchar(40),
  PRIMARY KEY(`ioc_resource_type_id`)
)
ENGINE=INNODB;

-- Drop table document
DROP TABLE IF EXISTS `document`;

CREATE TABLE `document` (
  `document_id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(255) NOT NULL DEFAULT '0',
  `document_title` varchar(255),
  `document_type` varchar(50),
  PRIMARY KEY(`document_id`)
)
ENGINE=INNODB;

-- Drop table signal_source
DROP TABLE IF EXISTS `signal_source`;

CREATE TABLE `signal_source` (
  `signal_source_id` int(11) NOT NULL AUTO_INCREMENT,
  `signal_source` varchar(50),
  PRIMARY KEY(`signal_source_id`)
)
ENGINE=INNODB;

-- Drop table vendor
DROP TABLE IF EXISTS `vendor`;

CREATE TABLE `vendor` (
  `vendor_id` int(11) NOT NULL AUTO_INCREMENT,
  `vendor_name` varchar(100) NOT NULL,
  PRIMARY KEY(`vendor_id`)
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

-- Drop table ioc_error_message
DROP TABLE IF EXISTS `ioc_error_message`;

CREATE TABLE `ioc_error_message` (
  `ioc_error_message_id` int(11) NOT NULL AUTO_INCREMENT,
  `ioc_error_message` varchar(250),
  PRIMARY KEY(`ioc_error_message_id`)
)
ENGINE=INNODB;

-- Drop table workflow
DROP TABLE IF EXISTS `workflow`;

CREATE TABLE `workflow` (
  `workflow_id` int(11) NOT NULL AUTO_INCREMENT,
  `workflow_tmplt_id` int(11),
  `workflow_no` varchar(50) NOT NULL DEFAULT '0',
  `workflow_start_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `workflow_completion_date` timestamp,
  `workflow_status` varchar(50),
  PRIMARY KEY(`workflow_id`),
  CONSTRAINT `Ref_233` FOREIGN KEY (`workflow_tmplt_id`)
    REFERENCES `workflow_tmplt`(`workflow_tmplt_id`)
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

-- Drop table renamed_pv
DROP TABLE IF EXISTS `renamed_pv`;

CREATE TABLE `renamed_pv` (
  `renamed_pv_id` int(11) NOT NULL AUTO_INCREMENT,
  `pv_id` int(11) DEFAULT '0',
  `new_pv_name` varchar(50),
  `old_pv_name` varchar(50),
  `old_pv_desc` varchar(255),
  `old_pv_end_date` datetime,
  PRIMARY KEY(`renamed_pv_id`),
  CONSTRAINT `Ref_195` FOREIGN KEY (`pv_id`)
    REFERENCES `pv`(`pv_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table task_tmplt
DROP TABLE IF EXISTS `task_tmplt`;

CREATE TABLE `task_tmplt` (
  `task_tmplt_id` int(11) NOT NULL AUTO_INCREMENT,
  `workflow_tmplt_id` int(11) NOT NULL DEFAULT '0',
  `task_op` varchar(50) NOT NULL DEFAULT '0',
  `task_description` text,
  `task_order` int(11),
  `task_lock` int(11),
  PRIMARY KEY(`task_tmplt_id`),
  CONSTRAINT `Ref_232` FOREIGN KEY (`workflow_tmplt_id`)
    REFERENCES `workflow_tmplt`(`workflow_tmplt_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table workflow_tmplt_hdr
DROP TABLE IF EXISTS `workflow_tmplt_hdr`;

CREATE TABLE `workflow_tmplt_hdr` (
  `workflow_tmplt_hdr_id` int(11) NOT NULL AUTO_INCREMENT,
  `workflow_tmplt_id` int(11) NOT NULL DEFAULT '0',
  `workflow_tmplt_hdr_text` varchar(50),
  `workflow_tmplt_hdr_content` text NOT NULL,
  `workflow_tmplt_hdr_order` int(11),
  `workflow_tmplt_hdr_description` text,
  `sign_off_required` int(11),
  PRIMARY KEY(`workflow_tmplt_hdr_id`),
  CONSTRAINT `Ref_231` FOREIGN KEY (`workflow_tmplt_id`)
    REFERENCES `workflow_tmplt`(`workflow_tmplt_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
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

-- Drop table cmpnt_type_prop_type_enum
DROP TABLE IF EXISTS `cmpnt_type_prop_type_enum`;

CREATE TABLE `cmpnt_type_prop_type_enum` (
  `cmpnt_type_prop_type_enum_id` int(11) NOT NULL AUTO_INCREMENT,
  `cmpnt_type_prop_type_id` int(11),
  `cmpnt_type_prop_type_enum` varchar(255),
  PRIMARY KEY(`cmpnt_type_prop_type_enum_id`),
  CONSTRAINT `Ref_193` FOREIGN KEY (`cmpnt_type_prop_type_id`)
    REFERENCES `cmpnt_type_prop_type`(`cmpnt_type_prop_type_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table elog_entry
DROP TABLE IF EXISTS `elog_entry`;

CREATE TABLE `elog_entry` (
  `elog_entry_id` int(11) NOT NULL AUTO_INCREMENT,
  `elog_book_id` int(11),
  `author` varchar(50) NOT NULL DEFAULT 'anon',
  `elog_entry` text,
  `elog_thread` int(11) NOT NULL DEFAULT '0',
  `elog_entry_create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY(`elog_entry_id`),
  CONSTRAINT `Ref_166` FOREIGN KEY (`elog_book_id`)
    REFERENCES `elog_book`(`elog_book_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table interface
DROP TABLE IF EXISTS `interface`;

CREATE TABLE `interface` (
  `interface_id` int(11) NOT NULL AUTO_INCREMENT,
  `install_rel_type_id` int(11) NOT NULL,
  `interface` varchar(100),
  PRIMARY KEY(`interface_id`),
  INDEX `idx_cmpnt_rel_type_id`(`install_rel_type_id`),
  UNIQUE INDEX `idx_interface_cmpnt_rel_type`(`install_rel_type_id`, `interface`),
  CONSTRAINT `cmpntreltype__interface_ibfk_1` FOREIGN KEY (`install_rel_type_id`)
    REFERENCES `install_rel_type`(`install_rel_type_id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT
)
ENGINE=INNODB;

-- Drop table alias
DROP TABLE IF EXISTS `alias`;

CREATE TABLE `alias` (
  `alias_id` int(11) NOT NULL AUTO_INCREMENT,
  `pv_id` int(11) NOT NULL DEFAULT '0',
  `alias` varchar(50),
  PRIMARY KEY(`alias_id`),
  CONSTRAINT `Ref_185` FOREIGN KEY (`pv_id`)
    REFERENCES `pv`(`pv_id`)
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
  PRIMARY KEY(`install_id`),
  CONSTRAINT `Ref_99` FOREIGN KEY (`cmpnt_type_id`)
    REFERENCES `cmpnt_type`(`cmpnt_type_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table vuri
DROP TABLE IF EXISTS `vuri`;

CREATE TABLE `vuri` (
  `vuri_id` int(11) NOT NULL AUTO_INCREMENT,
  `uri_id` int(11),
  PRIMARY KEY(`vuri_id`),
  INDEX `idx_uri_id`(`uri_id`),
  CONSTRAINT `Ref_50` FOREIGN KEY (`uri_id`)
    REFERENCES `uri`(`uri_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table ioc
DROP TABLE IF EXISTS `ioc`;

CREATE TABLE `ioc` (
  `ioc_id` int(11) NOT NULL AUTO_INCREMENT,
  `ioc_status_id` int(11),
  `ioc_nm` varchar(255),
  `system` varchar(255),
  `ioc_boot_instructions` text,
  `modified_by` varchar(50),
  `modified_date` timestamp,
  PRIMARY KEY(`ioc_id`),
  UNIQUE INDEX `ioc_nm`(`ioc_nm`),
  CONSTRAINT `Ref_202` FOREIGN KEY (`ioc_status_id`)
    REFERENCES `ioc_status`(`ioc_status_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table ioc_boot
DROP TABLE IF EXISTS `ioc_boot`;

CREATE TABLE `ioc_boot` (
  `ioc_boot_id` int(11) NOT NULL AUTO_INCREMENT,
  `ioc_id` int(11),
  `sys_boot_line` varchar(127),
  `ioc_boot_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `current_load` tinyint(1),
  `current_boot` tinyint(1),
  `modified_date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `modified_by` varchar(10),
  `boot_device` varchar(50),
  `boot_params_version` float,
  `console_connection` varchar(127),
  `host_inet_address` varchar(127),
  `host_name` varchar(127),
  `ioc_inet_address` varchar(127),
  `ioc_pid` int(11),
  `launch_script` varchar(127),
  `launch_script_pid` int(11),
  `os_file_name` varchar(127),
  `processor_number` int(11),
  `target_architecture` varchar(127),
  `ioc_status` varchar(50),
  PRIMARY KEY(`ioc_boot_id`),
  INDEX `idx_current_load`(`current_load`),
  INDEX `idx_ioc_id`(`ioc_id`),
  CONSTRAINT `Ref_54` FOREIGN KEY (`ioc_id`)
    REFERENCES `ioc`(`ioc_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table service_config
DROP TABLE IF EXISTS `service_config`;

CREATE TABLE `service_config` (
  `service_config_id` int(11) NOT NULL AUTO_INCREMENT,
  `service_id` int(11) NOT NULL DEFAULT '0',
  `service_config_name` varchar(50),
  `service_config_desc` varchar(255),
  `service_config_version` int(11),
  `service_config_create_date` timestamp,
  PRIMARY KEY(`service_config_id`),
  CONSTRAINT `Ref_197` FOREIGN KEY (`service_id`)
    REFERENCES `service`(`service_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table service_event
DROP TABLE IF EXISTS `service_event`;

CREATE TABLE `service_event` (
  `service_event_id` int(11) NOT NULL AUTO_INCREMENT,
  `service_config_id` int(11) NOT NULL DEFAULT '0',
  `service_event_user_tag` varchar(255),
  `service_event_UTC_time` timestamp NOT NULL DEFAULT now(),
  `service_event_serial_tag` int(11) DEFAULT '0',
  PRIMARY KEY(`service_event_id`),
  CONSTRAINT `Ref_08` FOREIGN KEY (`service_config_id`)
    REFERENCES `service_config`(`service_config_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table bundlepull__install
DROP TABLE IF EXISTS `bundlepull__install`;

CREATE TABLE `bundlepull__install` (
  `bundlepull__install_id` int(11) NOT NULL AUTO_INCREMENT,
  `bundle_pull_id` int(11) NOT NULL,
  `install_id` int(11) NOT NULL DEFAULT '0',
  `path_order` int(11),
  `validated` int(11),
  PRIMARY KEY(`bundlepull__install_id`),
  INDEX `idx_cable_pull_id`(`bundle_pull_id`),
  CONSTRAINT `Ref_57` FOREIGN KEY (`bundle_pull_id`)
    REFERENCES `bundle_pull`(`bundle_pull_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_76` FOREIGN KEY (`install_id`)
    REFERENCES `install`(`install_id`)
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
  `serial_no` varchar(255),
  PRIMARY KEY(`inventory_id`),
  INDEX `idx_cmpnt_type_id_c`(`cmpnt_type_id`),
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

-- Drop table ioc_prop
DROP TABLE IF EXISTS `ioc_prop`;

CREATE TABLE `ioc_prop` (
  `ioc_prop_id` int(11) NOT NULL AUTO_INCREMENT,
  `ioc_id` int(11),
  `ioc_proptype_id` int(11) NOT NULL DEFAULT '0',
  `ioc_prop_value` varchar(50),
  PRIMARY KEY(`ioc_prop_id`),
  CONSTRAINT `Ref_222` FOREIGN KEY (`ioc_id`)
    REFERENCES `ioc`(`ioc_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_223` FOREIGN KEY (`ioc_proptype_id`)
    REFERENCES `ioc_proptype`(`ioc_proptype_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table signal_desc
DROP TABLE IF EXISTS `signal_desc`;

CREATE TABLE `signal_desc` (
  `signal_desc_id` int(11) NOT NULL AUTO_INCREMENT,
  `signal_type_id` int(11),
  `signal_quality_id` int(11) NOT NULL,
  PRIMARY KEY(`signal_desc_id`),
  CONSTRAINT `Ref_248` FOREIGN KEY (`signal_type_id`)
    REFERENCES `signal_type`(`signal_type_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_249` FOREIGN KEY (`signal_quality_id`)
    REFERENCES `signal_quality`(`signal_quality_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table rec_client
DROP TABLE IF EXISTS `rec_client`;

CREATE TABLE `rec_client` (
  `rec_client_id` int(11) NOT NULL AUTO_INCREMENT,
  `rec_client_type_id` int(11),
  `rec_nm` varchar(128),
  `fld_type` varchar(24),
  `vuri_id` int(11),
  `current_load` tinyint(1),
  PRIMARY KEY(`rec_client_id`),
  INDEX `idx_rec_nm`(`rec_nm`),
  INDEX `FKIndex1`(`rec_client_type_id`),
  INDEX `idx_vuri_id`(`vuri_id`),
  CONSTRAINT `Ref_84` FOREIGN KEY (`rec_client_type_id`)
    REFERENCES `rec_client_type`(`rec_client_type_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_86` FOREIGN KEY (`vuri_id`)
    REFERENCES `vuri`(`vuri_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table cmpnttype__porttype
DROP TABLE IF EXISTS `cmpnttype__porttype`;

CREATE TABLE `cmpnttype__porttype` (
  `cmpnttype__porttype_id` int(11) NOT NULL AUTO_INCREMENT,
  `cmpnt_type_id` int(11) NOT NULL,
  `port_type_id` int(11) NOT NULL,
  `port_name` varchar(40) NOT NULL,
  `port_order` int(11) NOT NULL,
  PRIMARY KEY(`cmpnttype__porttype_id`),
  INDEX `idx_cmpnt_type_id_cpt`(`cmpnt_type_id`),
  INDEX `idx_port_type_id_cpt`(`port_type_id`),
  UNIQUE INDEX `idx_cmpnt_type_port_name_unique`(`cmpnt_type_id`, `port_name`),
  UNIQUE INDEX `idx_cmpnt_type_order_unique`(`cmpnt_type_id`, `port_order`),
  CONSTRAINT `cmpnttype__porttype_ibfk_1` FOREIGN KEY (`cmpnt_type_id`)
    REFERENCES `cmpnt_type`(`cmpnt_type_id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `cmpnttype__porttype_ibfk_2` FOREIGN KEY (`port_type_id`)
    REFERENCES `port_type`(`port_type_id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT
)
ENGINE=INNODB;

-- Drop table cmpnttype__interface
DROP TABLE IF EXISTS `cmpnttype__interface`;

CREATE TABLE `cmpnttype__interface` (
  `cmpnttype__interface_id` int(11) NOT NULL AUTO_INCREMENT,
  `cmpnt_type_id` int(11) NOT NULL,
  `interface_id` int(11) NOT NULL,
  `required` tinyint(1),
  `max_children` int(11) DEFAULT '0',
  PRIMARY KEY(`cmpnttype__interface_id`),
  INDEX `idx_cmpnt_type_id`(`cmpnt_type_id`),
  INDEX `idx_cmpnt_type_if_type_id`(`interface_id`, `cmpnt_type_id`),
  UNIQUE INDEX `idx_cmpnt_type_interface_unique`(`cmpnt_type_id`, `interface_id`, `required`),
  CONSTRAINT `cmpnt_type_if_ibfk_1` FOREIGN KEY (`cmpnt_type_id`)
    REFERENCES `cmpnt_type`(`cmpnt_type_id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `cmpnt_type_if_ibfk_3` FOREIGN KEY (`interface_id`)
    REFERENCES `interface`(`interface_id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT
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

-- Drop table inventory__document
DROP TABLE IF EXISTS `inventory__document`;

CREATE TABLE `inventory__document` (
  `inventory__document_id` int(11) NOT NULL AUTO_INCREMENT,
  `inventory_id` int(11),
  `document_id` int(11),
  PRIMARY KEY(`inventory__document_id`),
  CONSTRAINT `Ref_240` FOREIGN KEY (`document_id`)
    REFERENCES `document`(`document_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_241` FOREIGN KEY (`inventory_id`)
    REFERENCES `inventory`(`inventory_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table elogentry__document
DROP TABLE IF EXISTS `elogentry__document`;

CREATE TABLE `elogentry__document` (
  `elogentry__document_id` int(11) NOT NULL AUTO_INCREMENT,
  `elog_entry_id` int(11) NOT NULL DEFAULT '0',
  `document_id` int(11),
  PRIMARY KEY(`elogentry__document_id`),
  CONSTRAINT `Ref_237` FOREIGN KEY (`document_id`)
    REFERENCES `document`(`document_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_238` FOREIGN KEY (`elog_entry_id`)
    REFERENCES `elog_entry`(`elog_entry_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table ioc_error
DROP TABLE IF EXISTS `ioc_error`;

CREATE TABLE `ioc_error` (
  `ioc_error_id` int(11) NOT NULL AUTO_INCREMENT,
  `ioc_boot_id` int(11),
  `ioc_error_message_id` int(11),
  PRIMARY KEY(`ioc_error_id`),
  INDEX `idx_ioc_boot_id`(`ioc_boot_id`),
  INDEX `idx_ioc_error_num`(`ioc_error_message_id`),
  CONSTRAINT `ioc_error_ibfk_1` FOREIGN KEY (`ioc_boot_id`)
    REFERENCES `ioc_boot`(`ioc_boot_id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `Ref_77` FOREIGN KEY (`ioc_error_message_id`)
    REFERENCES `ioc_error_message`(`ioc_error_message_id`)
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

-- Drop table elogentry__elogtag
DROP TABLE IF EXISTS `elogentry__elogtag`;

CREATE TABLE `elogentry__elogtag` (
  `elogentry__elogtag_id` int(11) NOT NULL AUTO_INCREMENT,
  `elog_tag_id` int(11) NOT NULL DEFAULT '0',
  `elog_entry_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY(`elogentry__elogtag_id`),
  CONSTRAINT `Ref_128` FOREIGN KEY (`elog_tag_id`)
    REFERENCES `elog_tag`(`elog_tag_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_127` FOREIGN KEY (`elog_entry_id`)
    REFERENCES `elog_entry`(`elog_entry_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table elogentry__install
DROP TABLE IF EXISTS `elogentry__install`;

CREATE TABLE `elogentry__install` (
  `elogentry__install_id` int(11) NOT NULL AUTO_INCREMENT,
  `install_id` int(11) NOT NULL DEFAULT '0',
  `elog_entry_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY(`elogentry__install_id`),
  CONSTRAINT `Ref_130` FOREIGN KEY (`install_id`)
    REFERENCES `install`(`install_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_131` FOREIGN KEY (`elog_entry_id`)
    REFERENCES `elog_entry`(`elog_entry_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table iocboot_prop
DROP TABLE IF EXISTS `iocboot_prop`;

CREATE TABLE `iocboot_prop` (
  `iocboot_prop_id` int(11) NOT NULL AUTO_INCREMENT,
  `ioc_boot_id` int(11),
  `ioc_proptype_id` int(11),
  `ioc_prop` varchar(255),
  PRIMARY KEY(`iocboot_prop_id`),
  CONSTRAINT `Ref_196` FOREIGN KEY (`ioc_proptype_id`)
    REFERENCES `iocboot_proptype`(`iocboot_proptype_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_199` FOREIGN KEY (`ioc_boot_id`)
    REFERENCES `ioc_boot`(`ioc_boot_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table cmpnttype__doc
DROP TABLE IF EXISTS `cmpnttype__doc`;

CREATE TABLE `cmpnttype__doc` (
  `cmpnttype__doc_id` int(11) NOT NULL AUTO_INCREMENT,
  `doc_id` int(11),
  `cmpnt_type_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY(`cmpnttype__doc_id`),
  CONSTRAINT `Ref_148` FOREIGN KEY (`doc_id`)
    REFERENCES `doc`(`doc_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_159` FOREIGN KEY (`cmpnt_type_id`)
    REFERENCES `cmpnt_type`(`cmpnt_type_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table pv__install
DROP TABLE IF EXISTS `pv__install`;

CREATE TABLE `pv__install` (
  `pv__install_id` int(11) NOT NULL AUTO_INCREMENT,
  `pv_id` int(11) NOT NULL DEFAULT '0',
  `install_id` int(11) NOT NULL DEFAULT '0',
  `handle` varchar(50) DEFAULT NULL,
  PRIMARY KEY(`pv__install_id`),
  INDEX `idx_pv_id`(`pv_id`),
  INDEX `idx_install_id`(`install_id`),
  CONSTRAINT `Ref_111` FOREIGN KEY (`pv_id`)
    REFERENCES `pv`(`pv_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_116` FOREIGN KEY (`install_id`)
    REFERENCES `install`(`install_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table task
DROP TABLE IF EXISTS `task`;

CREATE TABLE `task` (
  `task_id` int(11) NOT NULL AUTO_INCREMENT,
  `workflow_id` int(11) NOT NULL DEFAULT '0',
  `task_tmplt_id` int(11) NOT NULL DEFAULT '0',
  `task_start_date` datetime,
  `task_completion_date` datetime,
  `task_status` int(11),
  `task_done_by` varchar(50) NOT NULL DEFAULT '0',
  `dr` int(11),
  PRIMARY KEY(`task_id`),
  CONSTRAINT `Ref_168` FOREIGN KEY (`workflow_id`)
    REFERENCES `workflow`(`workflow_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_239` FOREIGN KEY (`task_tmplt_id`)
    REFERENCES `task_tmplt`(`task_tmplt_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table pv_rel
DROP TABLE IF EXISTS `pv_rel`;

CREATE TABLE `pv_rel` (
  `pv_rel_id` int(11) NOT NULL AUTO_INCREMENT,
  `rel_type` varchar(50),
  `parent_pv_id` int(11) NOT NULL DEFAULT '0',
  `child_pv_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY(`pv_rel_id`),
  CONSTRAINT `Ref_154` FOREIGN KEY (`parent_pv_id`)
    REFERENCES `pv`(`pv_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_155` FOREIGN KEY (`child_pv_id`)
    REFERENCES `pv`(`pv_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table pv_attr
DROP TABLE IF EXISTS `pv_attr`;

CREATE TABLE `pv_attr` (
  `pv_attr_id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  `pv_id` int(11) NOT NULL DEFAULT '0',
  `pv_attrtype_id` int(11),
  `pv_attr` varchar(255),
  PRIMARY KEY(`pv_attr_id`),
  CONSTRAINT `Ref_151` FOREIGN KEY (`pv_id`)
    REFERENCES `pv`(`pv_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_118` FOREIGN KEY (`pv_attrtype_id`)
    REFERENCES `pv_attrtype`(`pv_attrtype_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table inventory__elogentry
DROP TABLE IF EXISTS `inventory__elogentry`;

CREATE TABLE `inventory__elogentry` (
  `inventory__elogentry_id` int(11) NOT NULL AUTO_INCREMENT,
  `inventory_id` int(11) NOT NULL DEFAULT '0',
  `elog_entry_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY(`inventory__elogentry_id`),
  CONSTRAINT `Ref_144` FOREIGN KEY (`inventory_id`)
    REFERENCES `inventory`(`inventory_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_145` FOREIGN KEY (`elog_entry_id`)
    REFERENCES `elog_entry`(`elog_entry_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table cabletype__partitiontype
DROP TABLE IF EXISTS `cabletype__partitiontype`;

CREATE TABLE `cabletype__partitiontype` (
  `cabletype__partitiontype` int(11) NOT NULL AUTO_INCREMENT,
  `cable_type_id` int(11),
  `partition_type_id` int(11) NOT NULL DEFAULT '0',
  `partition_preference` int(11),
  PRIMARY KEY(`cabletype__partitiontype`),
  INDEX `idx_tray_partition_type_id`(`partition_type_id`),
  CONSTRAINT `Ref_133` FOREIGN KEY (`partition_type_id`)
    REFERENCES `partition_type`(`partition_type_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_134` FOREIGN KEY (`cable_type_id`)
    REFERENCES `cable_type`(`cable_type_id`)
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

-- Drop table pvgroup__serviceconfig
DROP TABLE IF EXISTS `pvgroup__serviceconfig`;

CREATE TABLE `pvgroup__serviceconfig` (
  `pvgroup__serviceconfig_id` int(11) NOT NULL AUTO_INCREMENT,
  `pv_group_id` int(11) NOT NULL DEFAULT '0',
  `service_config_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY(`pvgroup__serviceconfig_id`),
  CONSTRAINT `Ref_09` FOREIGN KEY (`service_config_id`)
    REFERENCES `service_config`(`service_config_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_137` FOREIGN KEY (`pv_group_id`)
    REFERENCES `pv_group`(`pv_group_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table pv__pvgroup
DROP TABLE IF EXISTS `pv__pvgroup`;

CREATE TABLE `pv__pvgroup` (
  `pv__pvgroup_id` int(11) NOT NULL AUTO_INCREMENT,
  `pv_id` int(11) NOT NULL DEFAULT '0',
  `pv_group_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY(`pv__pvgroup_id`),
  INDEX `idx_pv_id`(`pv_id`),
  INDEX `idx_pvgroup_id`(`pv_group_id`),
  CONSTRAINT `Ref_92` FOREIGN KEY (`pv_id`)
    REFERENCES `pv`(`pv_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_95` FOREIGN KEY (`pv_group_id`)
    REFERENCES `pv_group`(`pv_group_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table task__elogentry
DROP TABLE IF EXISTS `task__elogentry`;

CREATE TABLE `task__elogentry` (
  `task__elogentry_id` int(11) NOT NULL AUTO_INCREMENT,
  `task_id` int(11) NOT NULL DEFAULT '0',
  `elog_entry_id` int(11),
  PRIMARY KEY(`task__elogentry_id`),
  CONSTRAINT `Ref_183` FOREIGN KEY (`task_id`)
    REFERENCES `task`(`task_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_194` FOREIGN KEY (`elog_entry_id`)
    REFERENCES `elog_entry`(`elog_entry_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table service__role
DROP TABLE IF EXISTS `service__role`;

CREATE TABLE `service__role` (
  `service__role_id` int(11) NOT NULL AUTO_INCREMENT,
  `service_id` int(11),
  `role_id` int(11),
  PRIMARY KEY(`service__role_id`),
  CONSTRAINT `Ref_173` FOREIGN KEY (`role_id`)
    REFERENCES `role`(`role_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_171` FOREIGN KEY (`service_id`)
    REFERENCES `service`(`service_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table iocboot__install
DROP TABLE IF EXISTS `iocboot__install`;

CREATE TABLE `iocboot__install` (
  `iocboot__install_id` int(11) NOT NULL AUTO_INCREMENT,
  `install_id` int(11),
  `ioc_boot_id` int(11),
  PRIMARY KEY(`iocboot__install_id`),
  CONSTRAINT `Ref_125` FOREIGN KEY (`install_id`)
    REFERENCES `install`(`install_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_203` FOREIGN KEY (`ioc_boot_id`)
    REFERENCES `ioc_boot`(`ioc_boot_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table vuri_rel
DROP TABLE IF EXISTS `vuri_rel`;

CREATE TABLE `vuri_rel` (
  `vuri_rel_id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_vuri_id` int(11),
  `child_vuri_id` int(11),
  `rel_info` text,
  PRIMARY KEY(`vuri_rel_id`),
  INDEX `idx_parent_vuri_id`(`parent_vuri_id`),
  INDEX `idx_child_vuri_id`(`child_vuri_id`),
  CONSTRAINT `Ref_51` FOREIGN KEY (`parent_vuri_id`)
    REFERENCES `vuri`(`vuri_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_64` FOREIGN KEY (`child_vuri_id`)
    REFERENCES `vuri`(`vuri_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table pgroup__role
DROP TABLE IF EXISTS `pgroup__role`;

CREATE TABLE `pgroup__role` (
  `pgroup__role_id` int(11) NOT NULL AUTO_INCREMENT,
  `pgroup_id` int(11),
  `role_id` int(11),
  PRIMARY KEY(`pgroup__role_id`),
  CONSTRAINT `Ref_163` FOREIGN KEY (`role_id`)
    REFERENCES `role`(`role_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_167` FOREIGN KEY (`pgroup_id`)
    REFERENCES `pgroup`(`pgroup_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table workflow__inventory
DROP TABLE IF EXISTS `workflow__inventory`;

CREATE TABLE `workflow__inventory` (
  `workflow__inventory` int(11) NOT NULL AUTO_INCREMENT,
  `workflow_id` int(11),
  `inventory_id` int(11),
  PRIMARY KEY(`workflow__inventory`),
  CONSTRAINT `Ref_153` FOREIGN KEY (`inventory_id`)
    REFERENCES `inventory`(`inventory_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_156` FOREIGN KEY (`workflow_id`)
    REFERENCES `workflow`(`workflow_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table install_partition_type
DROP TABLE IF EXISTS `install_partition_type`;

CREATE TABLE `install_partition_type` (
  `install_partition_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `install_id` int(11),
  `partition_type_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY(`install_partition_type_id`),
  CONSTRAINT `Ref_150` FOREIGN KEY (`install_id`)
    REFERENCES `install`(`install_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_152` FOREIGN KEY (`partition_type_id`)
    REFERENCES `partition_type`(`partition_type_id`)
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

-- Drop table person__pgroup
DROP TABLE IF EXISTS `person__pgroup`;

CREATE TABLE `person__pgroup` (
  `person__pgroup_id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11),
  `pgroup_id` int(11),
  PRIMARY KEY(`person__pgroup_id`),
  CONSTRAINT `Ref_161` FOREIGN KEY (`person_id`)
    REFERENCES `person`(`person_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_162` FOREIGN KEY (`pgroup_id`)
    REFERENCES `pgroup`(`pgroup_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table person__role
DROP TABLE IF EXISTS `person__role`;

CREATE TABLE `person__role` (
  `person__role_id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11),
  `role_id` int(11),
  PRIMARY KEY(`person__role_id`),
  CONSTRAINT `Ref_157` FOREIGN KEY (`role_id`)
    REFERENCES `role`(`role_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_160` FOREIGN KEY (`person_id`)
    REFERENCES `person`(`person_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table ioc_resource
DROP TABLE IF EXISTS `ioc_resource`;

CREATE TABLE `ioc_resource` (
  `ioc_resource_id` int(11) NOT NULL AUTO_INCREMENT,
  `ioc_boot_id` int(11),
  `text_line` varchar(255),
  `load_order` int(11),
  `uri_id` int(11),
  `unreachable` tinyint(1),
  `subst_str` varchar(255),
  `ioc_resource_type_id` int(11),
  PRIMARY KEY(`ioc_resource_id`),
  INDEX `idx_ioc_boot_id`(`ioc_boot_id`),
  INDEX `idx_uri_id`(`uri_id`),
  INDEX `idx_ioc_resource_type_id`(`ioc_resource_type_id`),
  CONSTRAINT `ioc_resource_ibfk_1` FOREIGN KEY (`ioc_boot_id`)
    REFERENCES `ioc_boot`(`ioc_boot_id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `ioc_resource_ibfk_2` FOREIGN KEY (`uri_id`)
    REFERENCES `uri`(`uri_id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `Ref_78` FOREIGN KEY (`ioc_resource_type_id`)
    REFERENCES `ioc_resource_type`(`ioc_resource_type_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table install_rel
DROP TABLE IF EXISTS `install_rel`;

CREATE TABLE `install_rel` (
  `install_rel_id` int(11) NOT NULL AUTO_INCREMENT,
  `install_rel_type_id` int(11),
  `parent_install_id` int(11) NOT NULL DEFAULT '0',
  `child_install_id` int(11) NOT NULL DEFAULT '0',
  `logical_desc` varchar(60),
  `logical_order` int(11),
  `install_date` timestamp,
  PRIMARY KEY(`install_rel_id`),
  INDEX `idx_cmpnt_rel_type_id`(`install_rel_type_id`),
  CONSTRAINT `cmpnt_rel_ibfk_3` FOREIGN KEY (`install_rel_type_id`)
    REFERENCES `install_rel_type`(`install_rel_type_id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
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

-- Drop table lattice
DROP TABLE IF EXISTS `lattice`;

CREATE TABLE `lattice` (
  `lattice_id` int(11) NOT NULL AUTO_INCREMENT,
  `model_line_id` int(11),
  `machine_mode_id` int(11),
  `model_geometry_id` int(11),
  `lattice_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `lattice_description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `created_by` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `create_date` datetime,
  `updated_by` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci,
  `update_date` datetime,
  PRIMARY KEY(`lattice_id`),
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
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table cmpnttype__cognizant
DROP TABLE IF EXISTS `cmpnttype__cognizant`;

CREATE TABLE `cmpnttype__cognizant` (
  `cmpnttype__cognizant_id` int(11) NOT NULL AUTO_INCREMENT,
  `cmpnt_type_id` int(11) DEFAULT '0',
  `person_id` int(11),
  `role_id` int(11),
  PRIMARY KEY(`cmpnttype__cognizant_id`),
  CONSTRAINT `Ref_190` FOREIGN KEY (`cmpnt_type_id`)
    REFERENCES `cmpnt_type`(`cmpnt_type_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_191` FOREIGN KEY (`person_id`)
    REFERENCES `person`(`person_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_182` FOREIGN KEY (`role_id`)
    REFERENCES `role`(`role_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table workflow__person
DROP TABLE IF EXISTS `workflow__person`;

CREATE TABLE `workflow__person` (
  `workflow__person_id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) DEFAULT '0',
  `workflow_id` int(11) DEFAULT '0',
  `role_id` int(11),
  PRIMARY KEY(`workflow__person_id`),
  CONSTRAINT `Ref_04` FOREIGN KEY (`workflow_id`)
    REFERENCES `workflow`(`workflow_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_170` FOREIGN KEY (`person_id`)
    REFERENCES `person`(`person_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_176` FOREIGN KEY (`role_id`)
    REFERENCES `role`(`role_id`)
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

-- Drop table elog_attachment
DROP TABLE IF EXISTS `elog_attachment`;

CREATE TABLE `elog_attachment` (
  `elog_attachment_id` int(11) NOT NULL AUTO_INCREMENT,
  `elog_entry_id` int(11) NOT NULL DEFAULT '0',
  `mime_type` varchar(50),
  `data` text,
  `url` varchar(50),
  PRIMARY KEY(`elog_attachment_id`),
  CONSTRAINT `Ref_175` FOREIGN KEY (`elog_entry_id`)
    REFERENCES `elog_entry`(`elog_entry_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table link_detail
DROP TABLE IF EXISTS `link_detail`;

CREATE TABLE `link_detail` (
  `link_detail_id` int(11) NOT NULL AUTO_INCREMENT,
  `install_rel_id` int(11) NOT NULL DEFAULT '0',
  `link_type` int(11),
  `port_port_connection_id` int(11),
  PRIMARY KEY(`link_detail_id`),
  CONSTRAINT `Ref_226` FOREIGN KEY (`install_rel_id`)
    REFERENCES `install_rel`(`install_rel_id`)
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

-- Drop table service_config_prop
DROP TABLE IF EXISTS `service_config_prop`;

CREATE TABLE `service_config_prop` (
  `service_config_prop_id` int(11) NOT NULL AUTO_INCREMENT,
  `service_config_id` int(11) NOT NULL DEFAULT '0',
  `service_config_prop_name` varchar(2555),
  `service_config_prop_value` varchar(255),
  PRIMARY KEY(`service_config_prop_id`),
  CONSTRAINT `Ref_12` FOREIGN KEY (`service_config_id`)
    REFERENCES `service_config`(`service_config_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table service_event_prop
DROP TABLE IF EXISTS `service_event_prop`;

CREATE TABLE `service_event_prop` (
  `service_event_prop_id` int(11) NOT NULL AUTO_INCREMENT,
  `service_event_id` int(11) NOT NULL DEFAULT '0',
  `service_event_prop_name` varchar(255),
  `service_event_prop_value` varchar(50),
  PRIMARY KEY(`service_event_prop_id`),
  CONSTRAINT `Ref_11` FOREIGN KEY (`service_event_id`)
    REFERENCES `service_event`(`service_event_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table masar_data
DROP TABLE IF EXISTS `masar_data`;

CREATE TABLE `masar_data` (
  `masar_data_id` int(11) NOT NULL AUTO_INCREMENT,
  `service_event_id` int(11) NOT NULL DEFAULT '0',
  `pv_name` varchar(50),
  `value` varchar(50),
  `status` int(11),
  `severity` int(11),
  `ioc_timestamp` int(11) UNSIGNED NOT NULL,
  `ioc_timestamp_nano` int(11) UNSIGNED NOT NULL,
  PRIMARY KEY(`masar_data_id`),
  CONSTRAINT `Ref_10` FOREIGN KEY (`service_event_id`)
    REFERENCES `service_event`(`service_event_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table task__document
DROP TABLE IF EXISTS `task__document`;

CREATE TABLE `task__document` (
  `task__document_id` int(11) NOT NULL AUTO_INCREMENT,
  `task_id` int(11) NOT NULL DEFAULT '0',
  `document_id` int(11),
  `dr` tinyint(1),
  PRIMARY KEY(`task__document_id`),
  CONSTRAINT `Ref_235` FOREIGN KEY (`document_id`)
    REFERENCES `document`(`document_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_234` FOREIGN KEY (`task_id`)
    REFERENCES `task`(`task_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table port
DROP TABLE IF EXISTS `port`;

CREATE TABLE `port` (
  `port_id` int(11) NOT NULL AUTO_INCREMENT,
  `cmpnttype__porttype_id` int(11),
  `install_id` int(11) NOT NULL DEFAULT '0',
  `port_field_label` varchar(100),
  PRIMARY KEY(`port_id`),
  INDEX `idx_port_type_id`(`cmpnttype__porttype_id`),
  CONSTRAINT `Ref_81` FOREIGN KEY (`install_id`)
    REFERENCES `install`(`install_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_229` FOREIGN KEY (`cmpnttype__porttype_id`)
    REFERENCES `cmpnttype__porttype`(`cmpnttype__porttype_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table pin
DROP TABLE IF EXISTS `pin`;

CREATE TABLE `pin` (
  `pin_id` int(11) NOT NULL AUTO_INCREMENT,
  `port_id` int(11),
  `signal_source_id` int(11),
  `pin_designator` varchar(50),
  PRIMARY KEY(`pin_id`),
  INDEX `idx_port_id_pp`(`port_id`),
  CONSTRAINT `pin_ibfk_2` FOREIGN KEY (`port_id`)
    REFERENCES `port`(`port_id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `Ref_250` FOREIGN KEY (`signal_source_id`)
    REFERENCES `signal_source`(`signal_source_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table rec_type
DROP TABLE IF EXISTS `rec_type`;

CREATE TABLE `rec_type` (
  `rec_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `ioc_boot_id` int(11),
  `rec_type` varchar(24),
  `ioc_resource_id` int(11),
  PRIMARY KEY(`rec_type_id`),
  INDEX `idx_ioc_boot_id`(`ioc_boot_id`),
  INDEX `idx_ioc_resource_id`(`ioc_resource_id`),
  CONSTRAINT `rec_type_ibfk_1` FOREIGN KEY (`ioc_boot_id`)
    REFERENCES `ioc_boot`(`ioc_boot_id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `rec_type_ibfk_2` FOREIGN KEY (`ioc_resource_id`)
    REFERENCES `ioc_resource`(`ioc_resource_id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT
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

-- Drop table cable
DROP TABLE IF EXISTS `cable`;

CREATE TABLE `cable` (
  `cable_id` int(11) NOT NULL AUTO_INCREMENT,
  `port_a_id` int(11),
  `port_b_id` int(11),
  `bundle_pull_id` int(11),
  `cable_type_id` int(11) NOT NULL DEFAULT '0',
  `color` varchar(60),
  `cable_identifier` varchar(50),
  `port_a_label` varchar(50),
  `port_b_label` varchar(50),
  `length_m` float,
  `continuity_check` int(11),
  `panel_to_device_check` int(11),
  PRIMARY KEY(`cable_id`),
  INDEX `idx_port_a_id`(`port_a_id`),
  INDEX `idx_port_b_id`(`port_b_id`),
  INDEX `idx_cable_pull_id`(`bundle_pull_id`),
  INDEX `idx_cable_type_id`(`cable_type_id`),
  CONSTRAINT `Ref_74` FOREIGN KEY (`port_a_id`)
    REFERENCES `port`(`port_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_75` FOREIGN KEY (`port_b_id`)
    REFERENCES `port`(`port_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_68` FOREIGN KEY (`bundle_pull_id`)
    REFERENCES `bundle_pull`(`bundle_pull_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_121` FOREIGN KEY (`cable_type_id`)
    REFERENCES `cable_type`(`cable_type_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table conductor
DROP TABLE IF EXISTS `conductor`;

CREATE TABLE `conductor` (
  `conductor_id` int(11) NOT NULL AUTO_INCREMENT,
  `cable_id` int(11) NOT NULL,
  `pin_a_id` int(11),
  `pin_b_id` int(11),
  `signal_desc_id` int(11),
  `signal_name` int(11),
  PRIMARY KEY(`conductor_id`),
  INDEX `idx_cable_id`(`cable_id`),
  INDEX `idx_pin_a_id`(`pin_a_id`),
  INDEX `idx_pin_b_id`(`pin_b_id`),
  CONSTRAINT `conductor_ibfk_1` FOREIGN KEY (`cable_id`)
    REFERENCES `cable`(`cable_id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `Ref_245` FOREIGN KEY (`signal_desc_id`)
    REFERENCES `signal_desc`(`signal_desc_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_246` FOREIGN KEY (`pin_b_id`)
    REFERENCES `pin`(`pin_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_247` FOREIGN KEY (`pin_a_id`)
    REFERENCES `pin`(`pin_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table rec_type_dev_sup
DROP TABLE IF EXISTS `rec_type_dev_sup`;

CREATE TABLE `rec_type_dev_sup` (
  `rec_type_dev_sup_id` int(11) NOT NULL AUTO_INCREMENT,
  `rec_type_id` int(11),
  `dtyp_str` varchar(24),
  `dev_sup_dset` varchar(50),
  `dev_sup_io_type` varchar(50),
  PRIMARY KEY(`rec_type_dev_sup_id`),
  CONSTRAINT `Ref_228` FOREIGN KEY (`rec_type_id`)
    REFERENCES `rec_type`(`rec_type_id`)
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

-- Drop table fld_type
DROP TABLE IF EXISTS `fld_type`;

CREATE TABLE `fld_type` (
  `fld_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `rec_type_id` int(11),
  `fld_type` varchar(24),
  `dbd_type` varchar(24),
  `def_fld_val` varchar(128),
  PRIMARY KEY(`fld_type_id`),
  INDEX `idx_dbd_type`(`dbd_type`),
  INDEX `idx_rec_type_id`(`rec_type_id`),
  CONSTRAINT `fld_type_ibfk_1` FOREIGN KEY (`rec_type_id`)
    REFERENCES `rec_type`(`rec_type_id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT
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

-- Drop table rec
DROP TABLE IF EXISTS `rec`;

CREATE TABLE `rec` (
  `rec_id` int(11) NOT NULL AUTO_INCREMENT,
  `ioc_boot_id` int(11),
  `rec_nm` varchar(128),
  `rec_type_id` int(11),
  PRIMARY KEY(`rec_id`),
  INDEX `idx_rec_nm`(`rec_nm`),
  INDEX `idx_ioc_boot_id`(`ioc_boot_id`),
  INDEX `idx_rec_type_id`(`rec_type_id`),
  CONSTRAINT `rec_ibfk_1` FOREIGN KEY (`ioc_boot_id`)
    REFERENCES `ioc_boot`(`ioc_boot_id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `rec_ibfk_2` FOREIGN KEY (`rec_type_id`)
    REFERENCES `rec_type`(`rec_type_id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT
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

-- Drop table rec_alias
DROP TABLE IF EXISTS `rec_alias`;

CREATE TABLE `rec_alias` (
  `rec_alias_id` int(11) NOT NULL AUTO_INCREMENT,
  `rec_id` int(11),
  `alias_nm` varchar(50),
  `ioc_resource_id` int(11),
  PRIMARY KEY(`rec_alias_id`),
  CONSTRAINT `Ref_205` FOREIGN KEY (`rec_id`)
    REFERENCES `rec`(`rec_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `Ref_206` FOREIGN KEY (`ioc_resource_id`)
    REFERENCES `ioc_resource`(`ioc_resource_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE=INNODB;

-- Drop table fld
DROP TABLE IF EXISTS `fld`;

CREATE TABLE `fld` (
  `fld_id` int(11) NOT NULL AUTO_INCREMENT,
  `rec_id` int(11),
  `fld_type_id` int(11),
  `fld_val` varchar(128),
  `ioc_resource_id` int(11),
  PRIMARY KEY(`fld_id`),
  INDEX `idx_fld_val`(`fld_val`),
  INDEX `idx_rec_id`(`rec_id`),
  INDEX `idx_fld_type_id`(`fld_type_id`),
  INDEX `idx_ioc_resource_id`(`ioc_resource_id`),
  CONSTRAINT `fld_ibfk_1` FOREIGN KEY (`rec_id`)
    REFERENCES `rec`(`rec_id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `fld_ibfk_2` FOREIGN KEY (`fld_type_id`)
    REFERENCES `fld_type`(`fld_type_id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `fld_ibfk_3` FOREIGN KEY (`ioc_resource_id`)
    REFERENCES `ioc_resource`(`ioc_resource_id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT
)
ENGINE=INNODB;

SET FOREIGN_KEY_CHECKS=1;
