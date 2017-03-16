#!/usr/bin/bash

#curl -L -O https://www.cs.uoregon.edu/Classes/17W/cis322/files/lost_data.tar.gz
#tar -zxvf lost_data.tar.gz

#rm -rf lost_data.tar.gz

#dropdb $1
#pg_ctl -D /home/osnapdev/CIS322/import -l logfile start
#createdb $1

#cd ..
#. preflight.sh $1
#cd import

#psql -d $1 -f import_data.sql 

if [ "$#" -ne 2 ]; then 
	echo "Usage: ./import_data.sh <dbname> <input_dir>"
	exit;
fi

python3 import_users.py $1 $2
