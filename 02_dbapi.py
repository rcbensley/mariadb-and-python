#!/usr/bin/env python3

import pymysql
import sqlite3


db_opts_mariadb = {'host': '127.0.0.1',
                   'database': 'test',
                   'autocommit': True,
                   'read_default_file': '~/.my.cnf'}

db_opts_sqlite = {'database': '/tmp/test.sqlite'}


sql_values = ",".join(list([f"({i})" for i in range(1, 11)]))
#  '(1),(2),(3),(4),(5),(6),(7),(8),(9),(10)'

sql = ("DROP TABLE IF EXISTS test_table;",
       "CREATE TABLE IF NOT EXISTS test_table(a int);",
       "INSERT INTO test_table (a) VALUES {sql_values}".format(sql_values=sql_values),
       "SELECT * FROM test_table;")


def query_db(driver, db_opts, sql):
    conn = driver.connect(**db_opts)
    cur = conn.cursor()
    for s in sql:
        cur.execute(s)
        rows = cur.fetchall()
        if rows:
            for row in rows:
                print(row)
    conn.close()


print("Query MariaDB:")
query_db(pymysql, db_opts_mariadb, sql)

print("Query SQLite:")
query_db(sqlite3, db_opts_sqlite, sql)
