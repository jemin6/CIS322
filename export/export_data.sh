#!/usr/bin/bash

if [ "$#" -ne 2]; then 
	echo "Usage: ./export_data.sh <dbname> <output_dir>"
	exit;
fi

