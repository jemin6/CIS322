#!/usr/bin/bash

if [ "$#" -ne 2 ]; then 
	echo "Usage: ./.sh <dbname> <output_dir>"
	exit;
fi

#If the directory does exist, the contents should be removed prior to generating the export files
if [ -d "$2" ]; then 
	rm -rf $2
fi

#Create the directory
mkdir $2

#accessing to the database 
#	-d, --dbname=DBNAME	datebase name to connect
#	-f, --file=FILENAME	execute commands from file then exit
#	-t, --tuples-only	print rows only 
psql -d $1 -f users.sql -t -A -F "," > $2/users.csv
psql -d $1 -f facilities.sql -t -A -F "," > $2/facilities.csv
psql -d $1 -f assets.sql -t -A -F "," > $2/assets.csv
psql -d $1 -f transfers.sql -t -A -F "," > $2/transfers.csv
