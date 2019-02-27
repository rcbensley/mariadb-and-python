DROP DATABASE IF EXISTS jam;
CREATE DATABASE jam;
USE jam;


DROP TABLE IF EXISTS t_jam_customers;
CREATE TABLE t_jam_customers (
	customer_id BIGINT(20) PRIMARY KEY NOT NULL,
	customer_name VARCHAR(128) NOT NULL
);

DROP TABLE IF EXISTS t_jam_orders;
CREATE TABLE t_jam_orders (
	order_id BIGINT(20) PRIMARY KEY NOT NULL,
	customer_id BIGINT(20) NOT NULL,
	product_id BIGINT(20) NOT NULL,
	qty INT(11) NOT NULL,
	order_date DATETIME NOT NULL
);

DROP TABLE IF EXISTS t_jam_products;
CREATE TABLE t_jam_products (
	product_id BIGINT(20) PRIMARY KEY NOT NULL,
	product_name VARCHAR(128) NOT NULL,
	price INT(11) NOT NULL
);

INSERT INTO t_jam_products VALUES (1, 'Strawberry Jam', 57),
	(2, 'Raspberry Jam', 59),
	(3, 'Banana Jam', 64), 
	(4, 'Cheese Jam', 123), 
	(5, 'Spam Jam', 99),
	(6, 'Ham Jam', 101),
	(7, 'Wham Jam', 77),
	(8, 'Thank You Jam', 77);

