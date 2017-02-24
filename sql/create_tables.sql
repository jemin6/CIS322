CREATE TABLE users (      /* table with username and password */
	user_pk		serial primary key,
	username        varchar(16),
	password        varchar(16)  /* Plaintext password  */
);

CREATE TABLE assets (
	asset_tag	varchar(16),
	description	text
);

CREATE TABLE facilities (
	fcode 		varchar(6),
	common_name	varchar(32)
);
