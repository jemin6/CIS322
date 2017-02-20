CREATE TABLE users (      /* table with username and password */
	user_pk         serial primary key,
	username        varchar(16),
	password        varchar(16),  /* Plaintext password  */
	active          boolean DEFAULT false
);
