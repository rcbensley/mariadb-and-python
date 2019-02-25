DROP DATABASE IF EXISTS jamalytics;
CREATE DATABASE jamalytics;
USE jamalytics;

CREATE TABLE `jam_summary` (
	order_id BIGINT(20) NOT NULL,
	customer_id BIGINT(20) NOT NULL,
	customer_name VARCHAR(128) NOT NULL,
	product_id BIGINT(20) NOT NULL,
	product_name VARCHAR(128) NOT NULL,
	price DECIMAL(10,2) NOT NULL,
	qty INT(11) NOT NULL,
	order_date DATETIME NOT NULL,
	price DECIMAL(64,2) NOT NULL
);
