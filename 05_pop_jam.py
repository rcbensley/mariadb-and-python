#!/usr/bin/env python3

from random import randint, randrange
from pprint import pprint as pp
from datetime import datetime as dt
from datetime import timedelta as td
import pymysql

TEST_SELECT = """
SELECT
    c.customer_name
    , p.product_name
    , SUM(p.price * o.qty) as total
FROM t_jam_orders o
JOIN t_jam_customers c ON o.customer_id = c.customer_id
JOIN t_jam_products p ON o.product_id = p.product_id
GROUP BY c.customer_name
"""


def biz_gen_500():
    def rand_name(names):
        return names[randint(0, (len(names)-1))]

    first = ('Mega', 'Humble', 'Friendly', 'Evil', 'Future',
             'Merciless', 'Dave', 'Cheese', 'Babs', 'Magic')
    second = ('Corp', 'Ltd', 'Inc', 'AB', 'Plc', 'Dynamics',
              '& Son', 'Global', 'Shop')
    biz = "{f} {s}".format(f=rand_name(first),
                           s=rand_name(second))
    return biz


def insert_table(cursor, table, values):
    for v in values:
        val_data = ",".join(
            [str(i) if i is int() else "'{}'".format(i) for i in v])
        s = "INSERT INTO {t} VALUES ({d})".format(t=table, d=val_data)
        cursor.execute(s)


def load(table, values, defaults_group, defaults_file="~/.my.cnf", ):
    c = pymysql.connect(autocommit=True,
                        read_default_file=defaults_file,
                        read_default_group=defaults_group)
    cur = c.cursor()
    cur.execute("DELETE FROM {}".format(table))
    insert_table(cur, table, values)
    cur.execute(TEST_SELECT)
    r = cur.fetchall()
    if r:
        pp(r)
    cur.close()
    c.close()


if __name__ == "__main__":

    CUSTOMERS = list()
    for i in range(1, 26):
        customer_id = i
        customer_name = biz_gen_500()
        customer = (customer_id, customer_name)
        print(customer)
        CUSTOMERS.append(customer)

    PRODUCTS = list(range(1, 9))

    def gen_orders(day_offset, denormalize=False,
                   order_count=10000, order_start=1):
        orders = []
        for i in range(order_start, order_count + order_start):
            customer_id = CUSTOMERS[randrange(0, len(CUSTOMERS))][0]
            product_id = PRODUCTS[randrange(0, len(PRODUCTS))]
            qty = randint(1, 200)
            day_offset += randint(1, 13)
            order_date = dt.today() - td(days=day_offset)
            order_date_str = order_date.strftime("%Y-%m-%d %H:%M:%S")
            o = [i, customer_id,
                 product_id, qty, order_date_str]
            orders.append(o)
        return orders

    NEW_ORDERS = gen_orders(day_offset=7, order_start=10001)
    ARCHIVE_ORDERS = gen_orders(day_offset=(3*365))

    print("Loading customers")
    load("t_jam_customers", CUSTOMERS, defaults_group='jam')
    load("t_jam_customers", CUSTOMERS, defaults_group='archive')

    print("Loading New Orders")
    load("t_jam_orders", NEW_ORDERS, defaults_group='jam')
    print("Loading Archive Orders")
    load("t_jam_orders", ARCHIVE_ORDERS, defaults_group='archive')
