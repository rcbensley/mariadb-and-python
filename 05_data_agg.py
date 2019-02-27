#!/usr/bin/env python3

import os
import pymysql


class JamSummaryReport:
    def __init__(self, defaults_group, defaults_file='~/.my.cnf'):

        self.defaults_file = defaults_file
        self.defaults_group = defaults_group

    def query(self, sql):
        db = pymysql.connect(autocommit=True,
                             local_infile=True,
                             read_default_file=self.defaults_file,
                             read_default_group=self.defaults_group)
        cur = db.cursor()
        try:
            cur.execute(sql)
            rows = cur.fetchall()
        finally:
            cur.close()

        if rows:
            return rows
        else:
            return None

    def delete_from_report(self):
        delete_sql = "DELETE FROM jam_report".format(**self.__dict__)
        self.query(delete_sql)

    def load_report(self, file_path):
        load_sql = ("LOAD DATA LOCAL INFILE '{outfile}'"
                    "INTO TABLE jam_report").format(outfile=file_path)
        self.query(load_sql)

    def dump_report(self, file_path):
        self.delete_outfile(file_path)

        sql = ("SELECT "
               "o.order_id"
               ", c.customer_id"
               ", c.customer_name"
               ", p.product_id"
               ", p.product_name"
               ", p.price"
               ", o.qty"
               ", o.order_date"
               ", SUM(p.price * o.qty) as total "
               "FROM t_jam_orders o "
               "JOIN t_jam_customers c ON o.customer_id = c.customer_id "
               "JOIN t_jam_products p ON o.product_id = p.product_id "
               "GROUP BY o.order_id "
               "ORDER BY o.order_id, o.order_date, c.customer_id, p.product_id"
               " INTO OUTFILE '{outfile}'").format(outfile=file_path)
        self.query(sql)

    def delete_outfile(self, file_path):
        if os.path.isfile(file_path):
            if os.access(file_path, os.W_OK):
                os.remove(file_path)


if __name__ == '__main__':
    # Archive data
    archive_file = "/tmp/jam_archive.tsv"
    db_archive = JamSummaryReport('archive')
    db_archive.dump_report(file_path=archive_file)

    # Production Data
    prod_file = "/tmp/jam_prod.tsv"
    db_new = JamSummaryReport('jam')
    db_new.dump_report(file_path=prod_file)

    db_analytics = JamSummaryReport('jamalytics')
    db_analytics.delete_from_report()
    db_analytics.load_report(file_path=archive_file)
    db_analytics.load_report(file_path=prod_file)
