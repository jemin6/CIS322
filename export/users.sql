/* Need to add users.active  */
\echo 'username,password,role,active'
SELECT users.username, users.password, roles.rolename
 FROM users LEFT JOIN roles ON role_fk=role_pk;
