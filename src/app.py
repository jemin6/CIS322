from flask import Flask, render_template, request, session, redirect
from config import dbname, dbhost, dbport
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
@app.route('/login_form',methods=['POST','GET'])
def login_form():
    if request.method=='GET':
        return render_template('login_form.html')
    if request.method=='POST':
        if 'username' in request.form and 'password' in request.form:
            user_name = request.form['username']
            user_password = request.form['password']
            SQL = "SELECT count(*) FROM users WHERE username=%s and password=%s"  #check login
            cursor.execute(SQL,(user_name,user_password))
            result = cursor.fetchone()[0]
            if result != 1:         #check if ID exist
                session['error'] = "ERROR: FAILED for %s."%user_name
                return redirect('error')
            session['username'] = request.form['username']
            return render_template('dashboard.html',username=session['username'])
        session['error'] = 'INVALID FORM FIELDS'
        return redirect('error')
    session['error'] = 'INVALID HTTP %s'%request.method
    return redirect('error')

#dashboard
@app.route('/dashboard',methods=('GET',))
def dashboard():
    return render_template('dashboard.html',username=session['username'])


#create user
@app.route('/create_user',methods=['POST','GET'])
def create_user():
    if request.method=='GET':
        return render_template('create_user.html')
    if request.method=='POST':
        if 'username' in request.form and 'password' in request.form:
            user_name = request.form['username']
            user_password = request.form['password']
            role = request.form['role']
            SQL = "SELECT * FROM users WHERE username=%s"
            cursor.execute(SQL,(user_name,))
            result = cursor.fetchone()
            print(result)
            if result:                     #if user name exist 
                session['error'] = 'Username <%s> is already taken.'%user_name
                return redirect('error')
            ADD = "SELECT role_pk FROM roles WHERE rolename=%s"
            cursor.execute(ADD,(role,))
            role_pk = cursor.fetchall()
            SQL= "INSERT INTO users (username,password,role_fk) VALUES (%s,%s,%s)"
            cursor.execute(SQL,(user_name,user_password,role_pk))
            conn.commit()
            session['error'] = 'Username <%s> is successfully added.'%user_name
            return redirect('error')
        session['error'] = 'INVALID FORM FIELDS'
        return redirect('error')
    session['error'] = 'INVALID HTTP %s'%request.method
    return redirect('error')

@app.route('/error',methods=('GET',))
def error():
    if 'error' in session.keys():
        msg = session['error']
        del session['error']
        return render_template('check_id.html',msg=msg)
    return render_template('check_id.html',msg='Unknown error')

@app.route('/add_facility',methods=['POST','GET'])
def add_facility():
    if request.method=='GET':
        return render_template('add_facility.html')
    if request.method=='POST':
        fcode = request.form['fcode']
        common_name = request.form['common_name']
        SQL = "SELECT common_name FROM facilities WHERE common_name=%s"
        cursor.execute(SQL,(common_name,))
        result = cursor.fetchall()
        print(result)
        if result:
            session['error'] = 'Already in database'
            return redirect('error')
        SQL = "INSERT INTO facilities (common_name,fcode) VALUES (%s,%s)"
        cursor.execute(SQL,(common_name,fcode))
        conn.commit()
        session['error'] = "Datebase successfully inserted into Facility"
    return render_template("add_facility.html",facilities=facilities) 

#add_asset
#@app.route('/add_asset',methods=['POST','GET'])
#def add_asset():
#    if request.method == 'GET':
#        return render_template('add_asset.html')
#    if request.method == 'POST':
#        asset_tag = request.form['asset_tag']
#        description = request.form['description']
#        facility = request.form['facility']
#        arrival_date = request.form['arrival_dt']
#        SQL ="SELECT asset_tag FROM assets WHERE asset_tag=%s"
#        cursor.execute(SQL,(asset_tag,))
#        result = cursor.fetchall()
#        if result:
#            session['error'] = 'Asset is already in database'
#            return redirect['error']
#        SQL = "INSERT INTO assets (asset_tag, description) VALUES (%s,%s)"
#        cursor.execute(SQL,(asset_tag,description))
#        SQL = "SELECT asset_pk FROM assets WHERE asset_tag=%s"
#        cursor.execute(SQL,(asset_tag,))
#        asset_pk = cursor.fetchall()
#        SQL = "SELECT facility_pk FROM facilities WHERE common_name=%s"
#        cursor.execute(SQL,(facility,))
#        facility_pk = cursor.fetchall()
#        SQL = "INSERT INTO asset_at (asset_fk, facility_fk, arrive_dt) VALUE (%s,%s,%s)"
#        cursor.execute(SQL,(asset_pk,facility_pk,arrival_dt))
#        conn.commit()
#        session['error'] = "Asset successfully inserted into database")
#        return redirect['error']





#logout
@app.route('/logout')
def logout():
    return render_template('logout.html')
    








if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
