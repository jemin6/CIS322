# This script handles the setup that must occur prior to run
# Specifically this script:
#    1. creates the database

if [ "$#" -ne 1 ]; then
		echo "Usage: ./preflight.sh <dbname>"
	fi 

	# Database prep
	cd sql
	psql $1 -f create_tables.sql

	cd ..


	cp -R src/* $HOME/wsgi   	#if we use app.py we don't need this line
