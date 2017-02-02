import csv
import psycopg2
import sys

# Connect to an existing database
conn = psycopg2.connect(dbname=sys.argv[1],host='127.0.0.1',port=int(sys.argv[2]))

# Open a cursor to perform database operations
cursor = conn.cursor()


def import_DC_inventory():
    with open('DC_inventory.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            asset_tag = row['asset tag']
            description = row['product']
            cursor.execute("INSERT INTO assets (asset_tag,description) VALUES (%s,%s)",(asset_tag,description,))
            conn.commit()
    return

def import_HQ_inventory():
    with open('HQ_inventory.csv','r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            asset_tag = row['asset tag']
            description = row['product']
            cursor.execute("INSERT INTO assets (asset_tag,description) VALUES (%s,%s)",(asset_tag,description,))
            conn.commit()
    return 

def import_NC_inventory():
    with open('NC_inventory.csv','r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            asset_tag = row['asset tag']
            description = row['product']
            cursor.execute("INSERT INTO assets (asset_tag,description) VALUES(%s,%s)",(asset_tag,description,))
            conn.commit()
    return 

def import_product_list():
    with open('product_list.csv','r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            vendor = row['vendor']
            cursor.execute("INSERT INTO products (vendor) VALUES(%s)",(vendor,))
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
import_NC_inventory()
import_product_list()
import_vendors()


# commit the changes to the database
conn.commit()

# close the connection nicely
cursor.close()
conn.close()

