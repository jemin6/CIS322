from flask import Flask, redirect, render_template, request, url_for, flash, session
from config import dbname, dbhost, dbport
import json
import psycopg2
from functools import wraps
import sys

app = Flask(__name__)
app.secret_key ="sample_secret_key"

# Connect to an existing database
conn = psycopg2.connect(dbname=dbname,host=dbhost,port=dbport)

# Open a cursor to perform database operations
cursor = conn.cursor()


def login_required(f):                 #access allowed when logged in. If not then not able to access. 
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("login required")
            return redirect(url_for('login_page'))
    return wrap


@app.route("/")
def main():
    return render_template("main.html", dbname=dbname, dbhost=dbhost, dbport=dbport)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    if request.method=='POST':
        if 'username' in request.form and 'password' in request.form:
            user_name = request.form['username']
            user_password = request.form['password']
            SQL = "SELECT password FROM users WHERE username=%s"  #check login
            cursor.execute(SQL,(user_name,))
            result = cursor.fetchall()
            if len(result) == 0:         #check if ID exist
                error="Invalid username"
            else:
                temp = False
                for password in result:
                    if password[0] == request.form['password']:
                        temp = True
                if not temp:
                    error="Invalid password"
                else:
                    session['username'] = request.form['username']
                    session['logged_in'] =True
                    session['role'] = 'test'
                    return render_template('dashboard.html',username=session['username'])
    return render_template('login.html', error=error)

@app.route("/dashboard",methods=('GET',))
@login_required
def dashboard():
    return render_template("dashboard.html",username=session['username'])


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
            result = cursor.fetchall()
            if len(result) == 0:
                SQL="SELECT role_pk FROM roles WHERE rolename=%s"
                cursor.execute(SQL,(role,))
                role_pk = cursor.fetchall()
                if len(role_pk) == 0:
                    SQL="INSERT INTO roles (rolename) VALUES (%s)"
                    cursor.execute(SQL,(role,))
                    SQL="SELECT role_pk FROM roles WHERE rolename=%s"
                    cursor.execute(SQL,(role,))
                    role_pk = cursor.fetchall()
                role_pk = role_pk[0][0]
                SQL= "INSERT INTO users (username,password,role_fk) VALUES (%s,%s,%s)"
                cursor.execute(SQL,(user_name,user_password,role_pk))
                conn.commit()
                flash("Successfully created username")
            else:
                flash("Already taken username")
    return render_template("create_user.html")

@app.route("/add_facility", methods=['GET', 'POST'])
@login_required
def add_facility():
    if request.method=='GET':
        return render_template('add_facility.html')
    cursor.execute("SELECT common_name FROM facilities")
    facilities=cursor.fetchall()
    if request.method=='POST':
        fcode = request.form['fcode']
        common_name = request.form['common_name']
        SQL="SELECT common_name FROM facilities WHERE common_name=%s"
        cursor.execute(SQL,(common_name,))
        result = cursor.fetchall()
        if len(result) == 0:
            SQL="INSERT INTO facilities (common_name, fcode) VALUES (%s,%s)"
            cursor.execute(SQL,(common_name,fcode))
            conn.commit()
            flash("Facility successfully inserted into database")
        else:
            flash("Facility already in database")
    return render_template("add_facility.html",username=session['username'], facilities=facilities)

@app.route("/add_asset", methods=['GET', 'POST'])
def add_asset():
    if request.method=='GET':
        return render_template("add_asset.html")
   
    cursor.execute("SELECT common_name FROM facilities")
    facilities = cur.fetchall()
    cursor.execute("SELECT asset_tag FROM assets")
    assets = cursor.fetchall()
    if request.method == 'POST':
        asset_tag = request.form['asset_tag']
        description = request.form['description']
        facility = request.form['facility']
        date = request.form['date']
        SQL="SELECT asset_tag FROM assets WHERE asset_tag=%s"
        cursor.exectue(SQL,(asset_tag,))
        result = cursor.fetchall()
        if len(results) == 0:
            SQL="INSERT INTO assets (asset_tag, description) VALUES (%s,%s)"
            cursor.execute(SQL,(asset_tag,description))
            SQL="SELECT asset_pk FROM assets WHERE asset_tag=%s"
            cursor.exectue(SQL,(asset_tag,))
            asset_pk = cursor.fetchall()
            SQL="SELECT facility_pk FROM facilities WHERE common_name=%s"
            cursor.execute(SQL,(facility,))
            facility_pk = cursor.fetchall()
            facility_pk = facility_pk[0]
            asset_pk = asset_pk[0]
            SQL="INSERT INTO asset_at (asset_fk, facility_fk, arrive_dt) VALUES (%s,%s,%s)"
            cursor.execute(SQL,(str(asset_pk[0]),str(facility_pk[0]),date))
            conn.commit()
            flash("Asset successfully inserted into database")
        else:
            flash("Asset already in database")
    return render_template("add_asset.html", facilities=facilities, assets=assets)


@app.route("/dispose_asset", methods=['GET', 'POST'])
@login_required
def disposeAsset():
    if request.method=='GET':
        return render_template('dispose_asset.html')
    if session['role'] != 'officer':
        if request.method == 'POST':
            asset_tag = request.form['asset_tag']
            date = request.form['date']
            SQL="SELECT asset_pk FROM assets WHERE asset_tag=%s"
            cursor.execte(SQL,(asset_tag,))
            result = cur.fetchall()
            if len(result) == 0:
                flash("asset does not exist")
            else:
                asset_pk = result[0]
                SQL="UPDATE asset_at SET depart_dt=%s WHERE asset_fk=%s"
                cursor.execute(SQL,(data,str(asset_pk[0])))
                conn.commit()
                flash("asset_tag disposed")
                return redirect(url_for("dashboard"))
        return render_template("dispose_asset.html")
    flash("Only logistics officers can dispose of assets")
    return render_template("main.html")


@app.route("/asset_report", methods=['GET', 'POST'])
@login_required
def assetReport():
    cursor.execute("SELECT common_name FROM facilities")
    facilities = cursor.fetchall()
    if request.method=='POST':
        facility = request.form['facility']
        date=request.form['data']
        try:
            cursor.execute("SELECT asset_tag, common_name, arrive_dt
            FROM assets a 
            JOIN asset_at aa ON asset_pk=asset_fk 
            INNER JOIN facilities ON facility_fk=facility_pk 
            WHERE facilities.common_name LIKE '%"+facility+"%' 
                AND '"+date+"' >= aa.arrive_dt 
                AND '"+date+"' <= aa.depart_dt;")
            data=cursor.fetchall()
        except Exception as e:
            flash('Please enter a Date')
    return render_template("asset_report.html", facilities=facilities, data=data)




@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for('main'))

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=8080, debug=True)
        

