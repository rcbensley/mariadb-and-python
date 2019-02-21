#!/usr/bin/env python3

import pymysql

CONNECTION_ARGS = {"host": "127.0.0.1",
                   "port": 3306,
                   "database": "mysql",
                   "read_default_file": "~/.my.cnf"}


def query(sql, connection_args: dict = CONNECTION_ARGS):
    db = pymysql.connect(**connection_args)
    cur = db.cursor()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
    finally:
        cur.close()

    return rows


def print_rows(header, rows):
    print(header)
    for i in rows:
        print(*i, sep="\t")


if __name__ == "__main__":
    SQL = (("Hostname", "SELECT @@hostname"),
           ("Version", "SELECT @@version"),
           ("WSREP", "SHOW GLOBAL STATUS LIKE 'WSREP%'"))

    for i in SQL:
        result = query(sql=i[1])
        print_rows(f"{i[0]}:", result)
