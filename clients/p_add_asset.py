# This client can be used to interact with the LOST interface prior to encryption
# implementation

import sys
import json
import datetime

# URL lib parts
from urllib.request import Request, urlopen
from urllib.parse   import urlencode

def main():
    # Check the CLI arguments
    if len(sys.argv)<6 :
        print("Usage: python3 %s <url> <vendor> <description> <compartments> <facility>"%sys.argv[0])
        return
                       
    args = dict()
    args['timestamp'] = datetime.datetime.utcnow().isoformat()
    args['vendor']  = sys.argv[2]
    args['description'] = sys.argv[3]
    args['compartments'] = sys.argv[4]
    args['facility'] = sys.argv[5]

    print("Adding asset matching:\n\tvendor: %s\n\tdesc: %s\n\tcompart: %s\n\tfacility: %s"%(args['vendor'],args['description'],args['compartments'],args['facility']))
    
    sargs = dict()
    sargs['arguments']=json.dumps(args)
    sargs['signature']=''
    data = urlencode(sargs)

    req = Request(sys.argv[1],data.encode('ascii'),method='POST')
    res = urlopen(req)

    resp = json.loads(res.read().decode('ascii'))

    print("Call to LOST returned: %s"%resp['result'])

if __name__=='__main__':
    main()
