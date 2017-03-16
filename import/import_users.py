import sys
import os
import csv
import psycopg2
from pathlib import Path
import re

conn = psycopg2.connect(dbname=sys.argv[1],host='127.0.0.1',port = 5432) 
cursor = conn.cursor()

def process_file(fname):
    p = Path(fname)
    name = p.name
    m = re.match('([^_]+)_inventory.csv',name)
    if not m:
        return 
    with p.open() as f:
        f.readline()
        for line in f:
            line = line.strip()
            print("%s,%s"%(m.group(1),line))

def import_users():
    with open(sys.argv[2]+"/users.csv",'r') as csvfile:
        users = csv.DictReader(csvfile)
        for row in users:
            username = row['username']
            password = row['password']
            role = row['role']
            SQL = "SELECT role_pk FROM roles WHERE rolename=%s"
            cursor.execute(SQL,(role,))
            role_num = cursor.fetchall()
            active = row['active']
            SQL = "INSERT INTO users (username,password,role_fk,active) VALUES (%s,%s,%s,%s)"
            cursor.execute(SQL,(username,password,role_num[0][0],active))
            conn.commit()
    return 
           
def main():
    import_users()

for arg in sys.argv[1:]:
    process_file(arg)

if __name__ =='__main__':
    main()
