This directory holds some tools for configuring the LOST database and migrating legacy OSNAP data.

Files: 
README.txt - This readme file
create_tables.sql - A script to generate the base tables
import_data.sh - A script to import some data into the base table
do_inserts.py - Python script to generate and import data


-------------------------------------
--  Example import_data.sh script
-------------------------------------
The demo import_data.sh script demonstrates how to import data using python to generate sql scripts. Here is output setting up and running the import_data.sh script.

[osnapdev@osnap-image sql]$ createdb mydb
[osnapdev@osnap-image sql]$ psql mydb -f create_tables.sql 
CREATE TABLE
CREATE TABLE
[osnapdev@osnap-image sql]$ bash import_data.sh mydb 5432
INSERT 0 1
INSERT 0 1
INSERT 0 1
INSERT 0 1
INSERT 0 1
[osnapdev@osnap-image sql]$ psql mydb
psql (9.5.5)
Type "help" for help.

mydb=# select * from users;


-----------------------------
-- python interacting with the database directly example
-----------------------------
[osnapdev@osnap-image sql]$ createdb mydb
[osnapdev@osnap-image sql]$ psql mydb -f create_tables.sql 
CREATE TABLE
CREATE TABLE
[osnapdev@osnap-image sql]$ python3 do_inserts.py mydb 5432
[osnapdev@osnap-image sql]$ psql mydb
psql (9.5.5)
Type "help" for help.

mydb=# select * from users;


mydb=#
