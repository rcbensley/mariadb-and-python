DROP DATABASE IF EXISTS jamalytics;
CREATE DATABASE jamalytics;
USE jamalytics;

CREATE TABLE `jam_summary` (
  `customer_name` varchar(128),
  `product_name` varchar(128),
  `total` decimal(42,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
