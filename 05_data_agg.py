#!/usr/bin/env python3

import os
import configparser

import pandas
import sqlalchemy


class JamSummaryReport:
    def __init__(self, cnf_path, cnf_section,
                 table_name=None, data_frame=None,
                 report_file_path="/tmp/jam_summary.csv"):
        uri_str = 'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'
        self.opts = self.read_cnf(cnf_path, cnf_section)
        self.uri = uri_str.format(**self.opts)
        self.table_name = table_name
        self.data_frame = data_frame
        self.report_file_path = report_file_path

    def __add__(self, external_data_frame):
        return self.data_frame + external_data_frame.data_frame

    def load_summary(self, file_path):
        self.dump_summary()

        e = sqlalchemy.create_engine(self.uri)
        e.execute()
        e.execute("DELETE FROM jam_summary")
        load_sql = ("LOAD DATA LOCAL INFILE '{report_file_path}'"
                    "INTO TABLE {table_name}").format(**self.__dict__)
        e.execute(load_sql)

    def get(self):
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
               "JOIN t_jam_products p ON o.product_id = p.product_id")
        self.data_frame = pandas.read_sql_query(sql, self.uri)

    def read_cnf(self, cnf_path, cnf_section):
        parser = configparser.ConfigParser()
        parser.read(os.path.expanduser(cnf_path))
        db_opts = dict(parser[cnf_section])
        return db_opts

    def dump_summary(self):
        self.data_frame.to_csv(path_or_buf=self.report_file_path,
                               header=False,
                               index=False, index_label=None,
                               sep="\t", quotechar='"',
                               line_terminator='\n', escapechar=None)


if __name__ == '__main__':
    # Archive data
    db_archive = JamSummaryReport('~/.my.cnf', 'archive')
    db_archive.get()

    # Production Data
    db_new = JamSummaryReport('~/.my.cnf', 'jam')
    db_new.get()

    # Merge archive with production
    report_df = db_archive + db_new

    # Connect to Analytics
    db_cs = JamSummaryReport('~/.my.cnf', 'jamalytics',
                             table_name='jam_summary',
                             df=report_df)

    # Load Report Into Analytics
    db_cs.load_summary()
