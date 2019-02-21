#!/usr/bin/env python3 -W ignore::DeprecationWarning

import os
import configparser

import pandas
import sqlalchemy


class Db:
    def __init__(self, uri: str):
        self.uri = uri
        self.engine = sqlalchemy.create_engine(self.uri)
        self.df = None

    def __add__(self, inbound_df):
        return self.df + inbound_df

    def get(self):
        self.df = pandas.read_sql_query('sql', self.engine)


def db_factory(rdbms, driver,
               cnf_path, cnf_section,
               opts: str = ''):
    '''Mash together a dict to create a uri string, to create a Db object'''
    c = read_cnf(cnf_path, cnf_section)
    c['rdbms'] = rdbms
    c['driver'] = driver
    c['opts'] = opts
    u = '{rdbms}+{driver}://{user}:{password}@{host}:{port}/{opts}'.format(**c)
    return Db(u)


def read_cnf(cnf_path, section):
    # cat ~/.file.cnf
    # [section_name]
    # host = a
    # port = b
    # user = c
    # password = d
    # database = e
    parser = configparser.ConfigParser()
    parser.read()
    db_opts = {parser[section][i]: i for i in (
        'host', 'port', 'user', 'password', 'database')}
    return db_opts


def cnf_path_str(cnf_name):
    return os.environ['HOME'] + f'/.{cnf_name}.cnf'


def upload(df, path):
    pass


if __name__ == '__main__':
    db_legacy = db_factory('mssql',
                           'pymssql',
                           cnf_path_str('legacy'),
                           'jam',
                           '?charset=utf8')
    db_new = db_factory('mysql',
                        'pymysql',
                        cnf_path_str('my'),
                        'jam')

    report_df = db_legacy + db_new
    upload(report_df)
