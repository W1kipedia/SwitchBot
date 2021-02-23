DROP DATABASE IF EXISTS `SwitchBot`; --you can rename these to whatever you want just make sure to watch out with this command
CREATE DATABASE `SwitchBot`;
USE `SwitchBot`;
SET NAMES UTF8;
SET character_set_client = utf8mb4;

CREATE TABLE `Boosters` (
    `client_id` VARCHAR(18) NOT NULL,
    `has custom role` BOOLEAN NOT NULL,
    `custom role name` VARCHAR(50) DEFAULT NULL,
    `custom role id` BIGINT(18) UNSIGNED DEFAULT NULL
) ENGINE=INNODB DEFAULT CHARSET=UTF8MB4 COLLATE=UTF8MB4_0900_AI_CI;

CREATE TABLE `Economy` (
	`client_id` VARCHAR(18) NOT NULL,
	`wallet` BIGINT(18) UNSIGNED NOT NULL,
    `bank` BIGINT(18) UNSIGNED NOT NULL
) ENGINE=INNODB DEFAULT CHARSET=UTF8MB4 COLLATE=UTF8MB4_0900_AI_CI;
