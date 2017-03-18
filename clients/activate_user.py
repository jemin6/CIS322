import sys
import json
import datetime

# URL lib parts
from urllib.request import Request, urlopen
from urllib.parse   import urlencode

def main():
    # Check the host part of the URL
    if len(sys.argv) < 5:
        print("Usage: python3 %s [host_url] [username] [password] [role]"%sys.argv[0])
        return

    # Second argument will be the username to create or reactivate
    if len(sys.argv[2]) > 16:
        print("Username: %s should be less than or equal to 16 characters."%sys.argv[2])
        return 

    # Third argument will be the password to set for the user.
    if len(sys.argv[3]) > 16:
        print("Password length should be less than or equal to 16 character.")
        return 

    # Fourth argument will be the role for the user 
    if(sys.argv[4] != 'facofc' and sys.argv[4] != 'logofc'):
        print("Role should be either facofc or logofc")
        return 

    print("User %s was successfully actiaved"%sys.argv[2])


