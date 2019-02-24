DROP TABLE IF EXISTS t_jam_customers
GO

CREATE TABLE t_jam_customers (
	customer_id BIGINT PRIMARY KEY NOT NULL,
	customer_name VARCHAR(128) NOT NULL
)
GO


DROP TABLE IF EXISTS t_jam_orders
GO

CREATE TABLE t_jam_orders (
	order_id BIGINT PRIMARY KEY NOT NULL,
	customer_id BIGINT NOT NULL,
	product_id BIGINT NOT NULL,
	qty INT NOT NULL,
	order_date DATETIME NOT NULL
)
GO


DROP TABLE IF EXISTS t_jam_products
GO

CREATE TABLE t_jam_products (
	product_id BIGINT PRIMARY KEY NOT NULL,
	product_name VARCHAR(128) NOT NULL,
	price DECIMAL(10,2) NOT NULL
)
GO


INSERT INTO t_jam_products VALUES (1, 'Strawberry Jam', 0.57),
	(2, 'Raspberry Jam', 0.59),
	(3, 'Banana Jam', 0.64), 
	(4, 'Cheese Jam', 1.23), 
	(5, 'Spam Jam', 0.99),
	(6, 'Ham Jam', 1.01),
	(7, 'Wham Jam', 0.77),
	(8, 'Thank You Jam', 0.77)
GO

