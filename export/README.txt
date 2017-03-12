Export directroy 

Export directory holds script 'export_data.sh'
Any other scripts needed to export data from your database. 
It will be run from $REPO/export with

	bash export_data.sh <dbname> <output dir>

- The first argument <dbname> will be the name of the database to export the data from. 
  The database server will be running on localhost (127.0.0.1 or /tmp) at port 5432.

- The second argument <output dir> with be the path for the directory where the data files should be written to. 
  If the directory does not exist, export_data.sh should create the directory. 
  If the directory does exist, the contents should be removed prior to generating the export files.


The following export files should be created by the export_data.sh script:

	users.csv - a csv file containing user information 
	facilities.csv - a csv file containing facility information
	assets.csv - a csv file containing assets information 
	transfers.csv - a csv file containing transfer information 

* users.csv - contains user information needed to reconstruct user accounts and is in CSV format
	username - login username
	password - login password
	role - user role (Logistics Officer or Facilities Officer)
	active - True if the user is currently allowed to login, otherwise False

* facilities.csv - contain the list of facilities and is in CSV format
	fcode - The facility code for the facility
	common_name - A more human friendly name for the facility

* assets.csv - lists the individual assets and is in CSV format
	asset_tag - The unique LOST asset tag for the asset
	description - A description of the asset
	facility - The initial facility the asset was located at
	acquired - The date the asset was acquired in ISO date format
	disposed - The date the asset was disposed in ISO date format or the string NULL

# NEED TO BE FIXED #
* transfers.csv - contains the history of motion for assets and is in CSV format
	asset_tag - The unique LOST asset tage for the asset
	request_by - The username of the user requesting the transfer
	request_dt - The date the request was submitted in ISO date format
	approve_by - The username of the user approving or rejecting the transfer
	approve_dt - The date the request was approved in ISO date format
	source - The fcode of the facility the asset started at
	destination - The fcode of the facility the asset moved to
	load_dt - The date the asset was loaded at the source in ISO date format
	unload_dt - The date the asset was unloaded at the destination in ISO date format


