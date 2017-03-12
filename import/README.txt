Import directory


Setup a fresh database and install your application

Import directory holds script 'import_data.sh' 
Any other scripts needed to import data from the data export files
Run from $REPO/import with

	bash import_data.sh <dbname> <input dir>

- The first argument <dbname> will be the name of the database to import the data into. 
  The database server will be running on localhost (127.0.0.1 or /tmp) at port 5432.

- The second argument <input dir> with be the path for the directory where the data files should be read from.


