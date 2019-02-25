#!/usr/bin/env python3

import os
import configparser

import pandas


class TableReport:
    def __init__(self, cnf_path, cnf_section, table_name=None, df=None):
        uri_str = 'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'
        self.opts = self.read_cnf(cnf_path, cnf_section)
        self.uri = uri_str.format(**self.opts)
        self.table_name = table_name
        if df is not None:
            self.db = df
        else:
            self.df = None

    def __add__(self, i):
        return self.df + i.df

    def get(self):
        sql = ("SELECT "
               "c.customer_name"
               ", p.product_name"
               ", SUM(p.price * o.qty) as total "
               "FROM t_jam_orders o "
               "JOIN t_jam_customers c ON o.customer_id = c.customer_id "
               "JOIN t_jam_products p ON o.product_id = p.product_id")
        self.df = pandas.read_sql_query(sql, self.uri)

    def read_cnf(self, cnf_path, cnf_section):
        parser = configparser.ConfigParser()
        parser.read(os.path.expanduser(cnf_path))
        db_opts = dict(parser[cnf_section])
        return db_opts

    def write(self):
        self.df.to_sql(self.table_name,
                       self.uri,
                       schema=self.opts['database'],
                       if_exists='replace',
                       index=True,
                       index_label=None,
                       chunksize=None,
                       dtype=None)


if __name__ == '__main__':
    db_archive = TableReport('~/.my.cnf', 'archive')
    db_archive.get()
    db_new = TableReport('~/.my.cnf', 'jam')
    db_new.get()
    report_df = db_archive + db_new
    db_cs = TableReport('~/.my.cnf', 'jamalytics', df=report_df)
    db_cs.write()
