DROP TABLE IF EXISTS t_jam_orders;
CREATE TABLE t_jam_orders (
	order_id BIGINT(20) PRIMARY KEY NOT NULL,
	customer_id BIGINT(20) NOT NULL,
	invoice_id BIGINT(20) NOT NULL,
	order_date DATETIME NOT NULL,
)

DROP TABLE IF EXISTS t_jam_invoices;
CREATE TABLE t_jam_invoices (
	invoice_id BIGINT(20) PRIMARY KEY NOT NULL,
	customer_id BIGINT(20) NOT NULL,
	product_id BIGINT(20) NOT NULL,
	qty INT(11) NOT NULL,
	price_id BIGINT(20) NOT NULL,
	invoice_date DATETIME NOT NULL
);

DROP TABLE IF EXISTS t_jam_products;
CREATE TABLE t_jam_products (
	product_id BIGINT(20) PRIMARY KEY NOT NULL,
	product_name BIGINT(20) NOT NULL,
);

DROP TABLE IF EXISTS t_jam_prices;
CREATE TABLE t_jam_prices (
	price_id BIGINT(20) PRIMARY KEY NOT NULL,
	price DECIMAL(10,20) NOT NULL
);