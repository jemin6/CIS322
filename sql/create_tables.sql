CREATE TABLE roles (
	role_pk		serial primary key, 	/* primary key for a role instance*/
	rolename	varchar(32)		/* short textual name for the role*/
);

INSERT INTO roles (rolename) VALUES ('Logistics Officer');
INSERT INTO roles (rolename) VALUES ('Facilities Officer');

CREATE TABLE users (      /* table with username and password */
	user_pk		serial primary key,
	username        varchar(16),
	password        varchar(16),  /* Plaintext password  */
	role_fk		integer REFERENCES roles(role_pk) not null, /* role foreign key */
	active		boolean DEFAULT true		/* Check true to allow login  */
);

CREATE TABLE assets (				/*table with assets */
	asset_pk	serial primary key,	
	asset_tag	varchar(16),		/* 16 characters in length */
	description	text			/* arbitrary length */
);

CREATE TABLE facilities (
	facility_pk 	serial primary key,
	fcode 		varchar(6),		/* facility code */
	common_name	varchar(32)		/* 32 characters in length */
);

CREATE TABLE asset_at (
	asset_fk        integer REFERENCES assets (asset_pk) not null, /* asset at a facility  */
	facility_fk     integer REFERENCES facilities (facility_pk) not null, /* facility the asset is at*/
	arrive_dt       timestamp, -- when the asset arrived
	depart_dt       timestamp, -- when the asset left
	acquired_dt	timestamp, -- when the asset acquired
	disposed_dt	timestamp -- when the asset disposed 
);

CREATE TABLE requests (
	request_pk 	serial primary key,     
	requester_fk 	integer REFERENCES roles(role_pk) not null, /* logistics officer submitting the request  */
	request_dt 	timestamp,	/* request time */
	approval_dt 	timestamp, 	/* approval time */
	source_fk 	integer REFERENCES facilities(facility_pk) not null, /* source facility */
	destination_fk	integer REFERENCES facilities(facility_pk) not null, /* destination facility */
	asset_fk 	integer REFERENCES assets(asset_pk) not null
);

CREATE TABLE transit(	/* table track assets in transit */
	transit_pk 	serial primary key,
	request_fk	integer REFERENCES requests(request_pk) not null, 
	load_time	timestamp,	/* time takse for load */
	unload_time	timestamp	/* time takes for unload */
);
