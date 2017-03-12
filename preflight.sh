# This script handles the setup that must occur prior to run
# Specifically this script:
#    1. creates the database
#    2. imports the legacy data
#    3. copies the required source to $HOME/wsgi

if [ "$#" -ne 1 ]; then
		echo "Usage: ./preflight.sh <dbname>"
	fi 

	# Database prep
	cd sql
	psql $1 -f create_tables.sql

	cd ..

	# Install the wsgi files 
	cp -R src/* $HOME/wsgi   	#if we use app.py we don't need this line
