CREATE DATABASE IF NOT EXISTS jamalytics;
USE jamalytics;

DROP TABLE IF EXISTS jam_report;
CREATE TABLE jam_report (
	order_id BIGINT(20) NOT NULL,
	customer_id BIGINT(20) NOT NULL,
	customer_name VARCHAR(128) NOT NULL,
	product_id BIGINT(20) NOT NULL,
	product_name VARCHAR(128) NOT NULL,
	price INT(11) NOT NULL,
	qty INT(11) NOT NULL,
	order_date DATETIME NOT NULL,
	total BIGINT(20) NOT NULL
);
