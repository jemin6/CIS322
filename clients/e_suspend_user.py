# This client can be used to interact with the LOST interface prior to encryption
# implementation

import sys
import json
import datetime
from osnap_crypto import decrypt, encrypt_and_sign

# URL lib parts
from urllib.request import Request, urlopen
from urllib.parse   import urlencode

def main():
    if len(sys.argv)<3 :
        print("Usage: python3 %s <hr.priv> <lost.pub> <url> <username>"%sys.argv[0])
        return

    args = dict()
    args['timestamp'] = datetime.datetime.utcnow().isoformat()
    args['username']  = sys.argv[4]

    print("Suspending user: %s"%args['username'])

    (data, sig, skey, nonce) = encrypt_and_sign(json.dumps(args), sys.argv[2], sys.argv[1])
    sargs = dict()
    sargs['arguments']=data
    sargs['signature']=sig
    data = urlencode(sargs)

    req = Request(sys.argv[3],data.encode('ascii'),method='POST')
    res = urlopen(req)

    data = decrypt(res.read(), skey, nonce)
    resp = json.loads(data)

    print("Call to LOST returned: %s"%resp['result'])

if __name__=='__main__':
    main()
