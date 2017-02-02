import csv
import psycopg2
import sys 

conn = psycopg2.connect(dbname=sys.argv[1],host='127.0.0.1',port=int(sys.argv[2]))
cursor = conn.cursor()

def import_DC_inventory():
    with open('DC_inventory.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            asset_tag = row['asset tag']
            cursor.execute("INSERT INTO assets (asset_tag) VALUES (%s)",(asset_tag,))
            conn.commit()
    return

def import_HQ_inventory():
    with open('HQ_inventory.csv','r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            asset_tag = row['asset tag']
            cursor.execute("INSERT INTO assets (asset_tag) VALUES (%s)",(asset_tag,))
            conn.commit()
    return

def import_vendors():
    with open('vendors.csv','r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            vendor = row['vendor']
            cursor.execute("INSERT INTO products (vendor) VALUES (%s)",(vendor,))
            conn.commit()
    return


import_DC_inventory()
import_HQ_inventory()
import_vendors()
