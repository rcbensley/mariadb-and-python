Watch this talk and many other cool talks:

* https://mariadb.com/openworks/sessions-on-demand/2019-getting-started-with-mariadb-and-python/
* https://mariadb.com/openworks/2019-sessions-on-demand/

# Getting Started with MariaDB and Python

* 01, Python and Amiga BASIC.
* 02, dbapi for everyone and every database.
* 03, read connection properties from a client config.
* 04, multiprocessing example from mqm.
* 05, export multiple results, in a format ready to be loaded into a ColumnStore table.

## Environment
My environment for the talk.

* FS-UAE, and Amiga Workbench 1.3! (the operating system is still available for purchase)
* A Valid MariaDB client config file, see 'example.cnf', mine is located at the default location:
```~/.my.cnf```
* I use Vim and Sublimetext to write code.
* Python 3.7, installed locally via homebrew for MacOS.
* MariaDB 10.3, install locally via homebrew for MacOS. This is where the jam and jam_archive tables live.
* Docker, to run MariaDB ColumnStore 1.2 on port 3307.

Running the docker image:
```
cd ~/path/to/mariadb-and-python
docker run -d --name jam -eMARIADB_USER=X -eMARIADB_PASSWORD=X -eMARIADB_DATABASE=jamalytics -p 3307:3306 -v ${PWD}:/sql --hostname jam mariadb/columnstore
```

This starts the MariaDB ColumnStore docker image under the name 'jam'.

## Databases
I import the three databases schemas from the command line:
```
mysql -P 3306 < schema_jam.sql
mysql -P 3306 < schema_jam_archive.sql
mysql -P 3307 < schema_jam_analytics.sql
```

# Runtime examples

## 01 Big Ben Bongs
The script only takes one command line parameter, and integer ranging from 1 to 12. Anything higher, lower, or not a number will produce an error message using 'sys.exit'.
```
$ ./01_bin_ben.py 5
BONG! BONG! BONG! BONG! BONG!
$ ./01_bin_ben.py five
five does not appear to be a number between 1 and 12
```

## 02 DBAPI example
Query both MariaDB using PyMySQL and SQLite3 (part of python standard library).
This script creates a table on both databases, for MariaDB the schema 'test' must be available and writable by the user in your config file.
Just run the script with no options, you should see this:
```
$ ./02_dbapi.py
Query MariaDB:
(1,)
(2,)
(3,)
(4,)
(5,)
(6,)
(7,)
(8,)
(9,)
(10,)
Query SQLite:
(1,)
(2,)
(3,)
(4,)
(5,)
(6,)
(7,)
(8,)
(9,)
(10,)
```

## 03 Reading the Client Config
Just a very basic exmaple, or selecting and reading data from my local MariaDB instance, and using the home config file to parse information to the driver to connect and query MariaDB.

## 04 Multi-Query-MariaDB
A working example based on another script I maintain to query multiple MariaDB servers at once using PyMySQL and Multiprocessing.
Here is a quick example, of querying both my local MariaDB and the ColumnStore in Docker:
```
./04_mqm.py --hosts=127.0.0.1:3306,127.0.0.1:3307 "select @@version,@@version_comment,now()"
```

## 05 Data Aggregation Example
This demo creates 2 files using the "SELECT ... INTO OUTFILE" command, and then loads them both into the ColumnStore using the "LOAD DATA LOCAL INFILE ... INTO TABLE ...".
In this example, the databases are doing all the work. THey are exporting data to disk, and running the imports. Python is just acting as a wrapper around these processes.
The end goal of any ETL/ELT and similar processes is to make them testable, repetable, and easy to expand.

The first script generates test data, and populate the tables in jam and jam_archive:
```
./05_pop_jam.py
```

The second script dumps and loads the data into ColumnStore:
```
./05_data_agg.py
```
