USE `SwitchBot`;

CREATE TABLE `Boosters` (
    `client_id` VARCHAR(18) NOT NULL,
    `has custom role` BOOLEAN NOT NULL,
    `custom role name` VARCHAR(50) DEFAULT NULL,
    `custom role id` BIGINT(18) UNSIGNED DEFAULT NULL
) ENGINE=INNODB DEFAULT CHARSET=UTF8MB4 COLLATE=UTF8MB4_0900_AI_CI;
