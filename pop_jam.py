#!/usr/bin/env python3 -W ignore::DeprecationWarning

import configparser
from random import randint
from pprint import pprint as pp
from datetime import datetime as dt
from datetime import timedelta as td
import pymysql
import pymssql

TEST_SELECT = """
SELECT
    c.customer_name
    , p.product_name
    , SUM(p.price * o.qty) as total
FROM t_jam_orders o
JOIN t_jam_customers c ON o.customer_id = c.customer_id
JOIN t_jam_products p ON o.product_id = p.product_id
GROUP BY c.customer_name, p.product_name
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
        val_data = ",".join([str(i) if i is int() else "'{}'".format(i) for i in v])
        s = "INSERT INTO {t} () VALUES ({d})".format(t=table, d=val_data)
        cursor.execute(s)


def load_new(table, values):
    c = pymysql.connect(database="jam", autocommit=True, read_default_file="~/.my.cnf")
    cur = c.cursor()
    cur.execute("DELETE FROM {}".format(table))
    insert_table(cur, table, values)
    cur.execute(TEST_SELECT)
    r = cur.fetchall()
    print("MariaDB")
    pp(r)
    cur.close()
    c.close()


def load_legacy(table, values):
    parser = configparser.ConfigParser()
    parser.read("~/.legacy.cnf")
    db_opts = {parser[section][i]: i for i in (
        'host', 'port', 'user', 'password', 'database')}
    c = pymssql.connect(**db_opts)
    cur = c.cursor()
    cur.execute("DELETE FROM {}".format(table))
    insert_table(cur, table, values)
    cur.execute(TEST_SELECT)
    r = cur.fetchall()
    print("MSSQL")
    pp(r)
    cur.close()
    cur.close()
    c.close()


def gen_orders(day_offset):
    orders = []
    for i in range(0, 1001):
        c = randint(0, 9)
        customer_id = CUSTOMERS[c][0]
        product_id = randint(1, 8)
        qty = randint(1, 200)
        order_date = dt.today() - td(days=day_offset)
        order_date_str = order_date.strftime("%Y-%m-%d %H:%M:%S")
        o = [i, customer_id, product_id, qty, order_date_str]
        orders.append(o)
    return orders


if __name__ == "__main__":
    CUSTOMERS = ([(randint(1, 1000), biz_gen_500()) for _ in range(1, 11)])
    NEW_ORDERS = gen_orders(day_offset=7)
    LEGACY_ORDERS = gen_orders(day_offset=(3*365))

    load_new("t_jam_customers", CUSTOMERS)
    load_legacy("t_jam_customers", CUSTOMERS)

    load_new("t_jam_orders", NEW_ORDERS)
    load_legacy("t_jam_orders", LEGACY_ORDERS)

