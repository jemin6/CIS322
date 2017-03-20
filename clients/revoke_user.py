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

    print("Revoke has been done")

if __name__=='__main__':
    main()
