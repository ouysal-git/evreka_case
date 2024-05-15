CREATE TABLE IF NOT EXISTS `devices` (
  `id` int(11) unsigned NOT NULL,
  `name` varchar(225) DEFAULT NULL,
  `ip_address` varchar(225) DEFAULT NULL,
  `port` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `location_history` (
  `id` int(11) unsigned NOT NULL,
  `latitude` double DEFAULT NULL,
  `longitude` double DEFAULT NULL,
  `time_stamp_` DATETIME DEFAULT CURRENT_TIMESTAMP
);