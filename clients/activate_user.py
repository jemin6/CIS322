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
        print("\n** ERROR **\nUSERNAME: %s \nCANNOT be more than 16 characters.\n\n"%sys.argv[2])
        return 

    # Third argument will be the password to set for the user.
    if len(sys.argv[3]) > 16:
        print("\n** ERROR **\nPASSWORD length should be less than or equal to 16 character.\n\n")
        return 

    # Fourth argument will be the role for the user 
    if(sys.argv[4] != 'facofc' and sys.argv[4] != 'logofc'):
        print("Role should be either facofc or logofc")
        return 


    args = dict()
    args['username'] = sys.argv[2]
    args['password'] = sys.argv[3]
    if sys.argv[4] == 'logofc':
        args['rolename'] = 'Logistics Officer'
    else: 
        args['rolename'] = 'Facilities Officer'
    data = urlencode(args)

    # Make the request.
    req = Request(sys.argv[1]+"create_user", data.encode('ascii'), method = 'POST')
    res = urlopen(req)

    # Print the result code
    print("%s"%res.read())

    #print("\n** SUCCESSFULLY ACTIVATED **\nUSERNAME: ",sys.argv[2], "\nROLE: ",sys.argv[4], "\n\n")

if __name__=='__main__':
    main()
