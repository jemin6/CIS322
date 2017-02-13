from flask import Flask, render_template, request, session, redirect, url_for
from config import dbname,dbhost,dbport
import json
import psycopg2



app = Flask(__name__)
app.secret_key ="sample_secret_key"

# Connect to an existing database
conn = psycopg2.connect(dbname=dbname,host=dbhost,port=dbport)

# Open a cursor to perform database operations
cursor = conn.cursor()

#login screen
@app.route('/')
def login_form():
    return render_template('login_form.html',dbname=dbname,dbhost=dbhost,dbport=dbport)


#login
@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        if(request.form['username']
                and request.form['password']):
            session['logged_in'] = True
            session['username'] = request.form['username']
            return request.form['username'] + " Welcome."
        else:
            return 'Invaild username/password.'
    else:
         return 'Wrong access'

#@app.route('rest/lost_key',methods=('POST',))
#def lost_key():
#    if request.method == 'POST':
        



@app.route('/rest/list_products',methods=('POST',))
def list_products():
    if request.method == 'POST' and 'arguments' in request.form:
        req = json.loads(request.form['arguments'])
    else:
        redirect('rest') 

    if len(req['compartments'])==0:
        print("have not compartment")
        SQLstart = """select vendor,description,string_agg(c.abbrv||':'||l.abbrv,',')from products p 
left join security_tags t on p.product_pk=t.product_fk 
left join sec_compartments c on t.compartment_fk=c.compartment_pk 
left join sec_levels l on t.level_fk=l.level_pk"""
        if req['vendor']=='' and req['description']=='':
            SQLstart += " group by vendor,description"
            cursor.execute(SQLstart)
        else:
            if not req['vendor']=='' and not req['description']=='':
                req['vendor']="%"+req['vendor']+"%"
                req['description']="%"+req['description']+"%"
                SQLstart += " where description ilike %s and vendor ilike %s group by vendor,description"
                cursor.execute(SQLstart,(req['description'],req['vendor']))
            elif req['vendor']=='':
                req['description']="%"+req['description']+"%"
                SQLstart += " where description ilike %s group by vendor,description"
                cursor.execute(SQLstart,(req['description'],))
            elif req['description']=='':
                req['vendor']="%"+req['vendor']+"%"
                SQLstart += " where vendor ilike %s group by vendor,description"
                cursor.execute(SQLstart,(req['vendor'],))
    else:
        print("have compartment %s"%len(req['compartments']))
        SQLstart = """select vendor,description,string_agg(c.abbrv||':'||l.abbrv,',') from security_tags t
left join sec_compartments c on t.compartment_fk=c.compartment_pk
left join sec_levels l on t.level_fk=l.level_pk
left join products p on t.product_fk=p.product_pk
where product_fk is not NULL and c.abbrv||':'||l.abbrv = ANY(%s)"""
        if req['vendor']=='' and req['description']=='':
            SQLstart += " group by vendor,description,product_fk having count(*)=%s"
            cursor.execute(SQLstart,(req['compartments'],len(req['compartments'])))
        else:
            if not req['vendor']=='' and not req['description']=='':
                req['vendor']="%"+req['vendor']+"%"
                req['description']="%"+req['description']+"%"
                SQLstart += " and description ilike %s and vendor ilike %s group by vendor,description,product_fk having count(*)=%s"
                cursor.execute(SQLstart,(req['compartments'],req['description'],req['vendor'],len(req['compartments'])))
            elif req['vendor']=='':
                req['description']="%"+req['description']+"%"
                SQLstart += " and description ilike %s group by vendor,description,product_fk having count(*)=%s"
                cursor.execute(SQLstart,(req['compartments'],req['description'],len(req['compartments'])))
            elif req['description']=='':
                req['vendor']="%"+req['vendor']+"%"
                SQLstart += " and vendor ilike %s group by vendor,description,product_fk having count(*)=%s"
                cursor.execute(SQLstart,(req['compartments'],req['vendor'],len(req['compartments'])))
    dbres = cursor.fetchall()
    listing = list()
    for row in dbres:
        e = dict()
        e['vendor'] = row[0]
        e['description'] = row[1]
        if row[2] is None:
            e['compartments'] = list()
        else:
            e['compartments'] = row[2].split(',')
        listing.append(e)
    dat = dict()
    dat['timestamp'] = req['timestamp']
    dat['listing'] = listing
    data = json.dumps(dat)

    conn.close()
    return data

@app.route('/rest/suspend_user',methods=('POST',))
def suspend_user():
    if request.method =='POST' and 'arguments' in request.form:
        req = json.loads(request.form['arguments'])

    dat = dict()
    dat['timestamp'] = req['timestamp']
    dat['result'] = 'OK'
    data = json.dumps(dat)
    return data


@app.route('/rest/activate_user',methods=('POST',))
def activate_user():
    if request.method =='POST' and 'arguments' in request.form:
        req = json.loads(request.form['arguments'])

    dat = dict()
    dat['timestamp'] = req['timestamp']
#    dat['username'] = req['username']
    dat['result'] = 'OK'
    data = json.dumps(dat)

    SQL = "INSERT INTO users (username) VALUES (%s)"
    data1 = (req['username'],)
    cursor.execute(SQL,data1)
    conn.commit()
    return data



@app.route('/rest/add_products',methods=('POST',))
def add_products():
    if request.method == 'POST' and 'arguments' in request.form:
        req = json.loads(request.form['arguments'])

    if len(sys.argv)<6 :
        return 

    # Prep the arguments blob
    args = dict()
    args['timestamp'] = req['timestamp']

    prod = dict()
    prod['vendor'] = sys.argv[2]
    prod['description'] = sys.argv[3]
    prod['alt_description'] = sys.argv[4]
    prod['compartments'] = sys.argv[5]
    prod_list = list()
    pro_list.append(prod)
    args['new_products'] = prod_list

    # Setup the data to send
    sargs = dict()
    sargs['arguments']=json.dumps(args)
    sargs['signature']=''
    data = urlencode(sargs)


    return data


#@app.route('/rest/add_products',methods=('POST',))
#def add_products():
#    if request.method == 'POST' and 'arguments' in request.form:
#        req = json.loads(request.form['arguments'])

#    if len(req['compartments'])==0:
#        print("have not compartment")
#        SQLstart = """select vendor, description,alt_description,string_agg(c.abbrv||':'||l.abbrv,',') from products p
#left join security_tags t on p.product_pk=t.product_fk
#left join sec_compartments c on t.compartment_fk=c.compartment_pk
#left join sec_levels l on t.level_fk=l.level_pk"""
#        if req['vendor']=='' and req['description']=='' and req['alt_description']=='':
#            SQLstart += "group by vendor,description,alt_description"
#            cursor.execute(SQLstart)
#        else:
#            if not req['vendor']=='' and not req['description']=='':
#                req['vendor']="%"+req['vendor']+"%"
#                req['description']="%"+req['description']+"%"
#                SQLstart += " where description ilike %s and vendor ilike %s group by vendor,description"
#                cursor.execute(SQLstart,(req['description'],req['vendor']))
#            elif req['vendor'] =='':
#                req['description']="%"+req['description']+"%"
#                SQLstart += " where description ilike %s group by vendor,description"
#                cur.execute(SQLstart,(req['description'],))
#            elif req['description']=='':
#                req['vendor']="%"+req['vendor']+"%"
#                SQLstart += " where vendor ilike %s group by vendor,description"
#                cursor.execute(SQLstart,(req['vendor'],))
#    else:
#        print("have compartment %s"%len(req['compartments']))
#        SQLstart = """select vendor,description,alt_description,string_agg(c.abbrv||':'||l.abbrv,',')
#        from security_tags t
#left join sec_compartments c on t.compartment_fk=c.compartment_pk
#left join sec_levels l on t.level_fk=l.level_pk
#left join products p on t.product_fk=p.product_pk
#where product_fk is not NULL and c.abbrv||':'||l.abbrv = ANY(%s)"""
#        if req['vendor']=='' and req['description']=='':
#            SQLstart += " group by vendor,description,product_fk having count(*)=%s"
#            cursor.execute(SQLstart,(req['compartments'],len(req['compartments'])))
#        else:
#            if not req['vendor']=='' and not req['description']=='':
#                req['vendor']="%"+req['vendor']+"%"
#                req['description']="%"+req['description']+"%"
#                SQLstart += " and description ilike %s and vendor ilike %s group by vendor,description,product_fk having count(*)=%s"
#                cursor.execute(SQLstart,(req['compartments'],req['description'],req['vendor'],len(req['compartments'])))
#            elif req['vendor']=='':
#                req['description']="%"+req['description']+"%"
#                SQLstart += " and description ilike %s group by vendor,description,product_fk having count(*)=%s"
#                cursor.execute(SQLstart,(req['compartments'],req['description'],len(req['compartments'])))
#            elif req['description']=='':
#                req['vendor']="%"+req['vendor']+"%"
#                SQLstart += " and vendor ilike %s group by vendor,description,product_fk having count(*)=%s"
#                cursor.execute(SQLstart,(req['compartments'],req['vendor'],len(req['compartments'])))

#    dbres = cursor.fetchall()
#    listing = list()
#    for row in dbres:
#        e = dict()
#        e['vendor'] = row[0]
#        e['description'] = row[1]
#        e['alt_description'] = row[2]
#        e['compartments'] = row[3]
#        listing.append(e)

    #prepare the response
#    dat = dict()
#    dat['timestamp'] = req['timestamp']
#    dat['result'] = 'OK'
#    data = json.dumps(dat)
    
#    conn.close()
#    return data

#report filter screen 
@app.route('/report_filter_screen/')
def report_filter_screen():     
        return render_template('report_filter_screen.html')


#facility inventory report
@app.route('/facility_inventory_report', methods =['POST','GET'])
def facility_inventory_report():
    SQL ="select * from assets"
    cursor.execute(SQL)
    result = cursor.fetchall()
    processed_data = []
    for r in result:
        processed_data.append(dict(zip(('column_name1', 'column_name2','column_name3','column_name4','column_name5'), r)) )
    session['result'] = processed_data
    #session['result'] = result
    conn.commit()
    return render_template('facility_inventory_report.html')





@app.route('/in_transit_report')
def in_transit_report():
    return render_template('in_transit_report.html')


@app.route('/logout')
def logout():
    return render_template('logout.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    
