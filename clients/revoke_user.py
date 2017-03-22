import sys
import json
import datetime

# URL lib parts
from urllib.request import Request, urlopen
from urllib.parse   import urlencode

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 %s [host_url] [username]"%sys.argv[0])
        return

    # Put the username into dictionary & encode.
    args = dict()
    args['username'] = sys.argv[2]
    data = urlencode(args)

    # Make the request.
    req = Request(sys.argv[1]+"revoke", data.encode('ascii'), method = 'POST')
    res = urlopen(req)

    print("%s"%res.read())

if __name__=='__main__':
    main()
