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

#import users 
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

#importing facilities
def import_facilities():
    with open(sys.argv[2]+"/facilities.csv",'r') as csvfile:
        facilities = csv.DictReader(csvfile)
        for row in facilities:
            fcode = row['fcode']
            common_name = row['common_name']
            SQL = "INSERT INTO facilities (fcode,common_name) VALUES (%s,%s)"
            cursor.execute(SQL,(fcode,common_name))
            conn.commit()
    return
 

#importing assets
def import_assets():
    with open(sys.argv[2]+"/assets.csv",'r') as csvfile:
        assets = csv.DictReader(csvfile)
        for row in assets:
            asset_tag = row['asset_tag']
            description = row['description']
            facility = row['facility']
            acquired = row['acquired']
            if acquired == "NULL": 
                acquired = None         # correct to null
            disposed = row['disposed']
            if disposed == "NULL":
                disposed = None
            SQL = "INSERT INTO assets (asset_tag,description) VALUES (%s,%s)"
            cursor.execute(SQL,(asset_tag,description))
            conn.commit()
            SQL = "SELECT asset_pk FROM assets WHERE asset_tag=%s"
            cursor.execute(SQL,(asset_tag,))
            asset_fk = cursor.fetchall()
            SQL = "SELECT facility_pk FROM facilities WHERE fcode=%s"
            cursor.execute(SQL,(facility,))
            facility_fk = cursor.fetchall()
            if len(facility_fk) == 0:
                print("Try to import asset into facility that doesn't exist {}".format(facility))
                continue
            SQL = "INSERT INTO asset_at (asset_fk, facility_fk, acquired_dt, disposed_dt) VALUES(%s,%s,%s,%s)"
            cursor.execute(SQL,(asset_fk[0][0],facility_fk[0][0],acquired, disposed))           
            conn.commit()
    return 

#Still need to be fixed 
#import transfer 
def import_transfers():
    with open(sys.argv[2]+"/transfers.csv",'r') as csvfile:
        transfers = csv.DictReader(csvfile)
        for row in transfers:
            asset_tag = row['asset_tag']
            SQL = "SELECT asset_pk FROM assets WHERE asset_tag=%s"
            cursor.execute(SQL,(asset_tag,))
            asset_fk = cursor.fetchall()
            #SQL = "INSERT INTO assets (asset_tag) VALUES (%s)"
            #cursor.execute(SQL,(asset_tag,))
            #conn.commit()
            request_by = row['request_by']
            #request_dt = row['request_dt']
            SQL = "INSERT INTO requests (requester_fk) VALUES (%s)"
            cursor.execute(SQL,(request_by,))
            conn.commit()
            #approve_by = row['approve_by']
            #SQL="INSERT INTO requests (approver_fk) VALUES (%s)"
            #cursor.execute(SQL,(approve_by,))
            #conn.commit()
            load_dt = row['load_dt']
            unload_dt = row['unload_dt']
            SQL="INSERT INTO transit (load_dt, unload_dt) VALUES (%s,%s)"
            cursor.execute(SQL,(load_dt,unload_dt))
            conn.commit()
            
    return 




def main():
    import_users()
    import_facilities()
    import_assets()
    import_transfers()

    
for arg in sys.argv[1:]:
    process_file(arg)

if __name__ =='__main__':
    main()
