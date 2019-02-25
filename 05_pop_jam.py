#!/usr/bin/env python3

from random import randint
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
        print("MariaDB")
        pp(r)
    cur.close()
    c.close()


def gen_orders(day_offset, denormalize=False):
    orders = []
    order_counter = 1
    while order_counter <= 1000:
        for c in CUSTOMERS:
            customer_id = c[0]
            for p in range(1, 9):
                product_id = p
                qty = randint(1, 200)
                day_offset += randint(1, 13)
                order_date = dt.today() - td(days=day_offset)
                order_date_str = order_date.strftime("%Y-%m-%d %H:%M:%S")
                o = [order_counter, customer_id,
                     product_id, qty, order_date_str]
                orders.append(o)
                order_counter += 1
    return orders


if __name__ == "__main__":
    CUSTOMERS = ([(randint(1, 1000), biz_gen_500()) for _ in range(1, 11)])
    NEW_ORDERS = gen_orders(day_offset=7)
    ARCHIVE_ORDERS = gen_orders(day_offset=(3*365))

    print("Loading mariadb customers")
    load("t_jam_customers", CUSTOMERS, defaults_group='jam')
    print("Loading archive customers")
    load("t_jam_customers", CUSTOMERS, defaults_group='archive')

    print("Loading mariadb orders")
    load("t_jam_orders", NEW_ORDERS, defaults_group='jam')
    print("Loading archive orders")
    load("t_jam_orders", ARCHIVE_ORDERS, defaults_group='archive')
