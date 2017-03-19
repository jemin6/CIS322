** This directory is to told m web service client implementations. 

	activate_user.py: One client will be implemented to create_users
	revoke_user.py: client will be implemented to revoke users

--------------------------------------------------------------------------
activate_user.py 

- Three arguments will be passed. 

- First argument will be the host part of the URL 
  for instance and will include a trailing '/' (e.g. http://127.0.0.1:8080/).

- Second argument will be the username to create or reactivate.

- Third argument will be the password to set for the user.	

- Fourth argument will be the role for the user facofc or logofc 
  for the facilities officer and logistics officer roles respectively.
--------------------------------------------------------------------------
revoke_user.py

- Two arguments will be passed to revoke_user.py.

- First argument will be the host part of the URL 
  for instance and will include a trailing '/' (e.g. http://127.0.0.1:8080/). 

- The second argument will be the username to revoke.


	python3 revoke_user.py http://127.0.0.1:8080/ smith14
--------------------------------------------------------------------------

