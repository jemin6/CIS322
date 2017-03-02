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


#def login_required(f):                 #access allowed when logged in. If not then not able to access. 
#    @wraps(f)
#    def wrap(*args, **kwargs):
#        if 'logged_in' in session:
#            return f(*args, **kwargs)
#        else:
#            flash("login required")
#            return redirect(url_for('login_page'))
#    return wrap


@app.route("/")
def main():
    return render_template("main.html", dbname=dbname, dbhost=dbhost, dbport=dbport)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form:
            user_name = request.form['username']
            SQL = "SELECT password FROM users WHERE username=%s"  #check login
            cursor.execute(SQL,(user_name,))
            result = cursor.fetchall()
            if len(result) == 0:
                error = "User does not exist"
            else:
                tmp = False
                for password in result:
                    if password[0] == request.form['password']:
                        tmp = True
                if not tmp:
                    error = "Invalid password"
                else:
                    session['username'] = request.form['username']
                    session['logged_in'] = True
                    session['role'] = 'test'
                    return redirect(url_for('dashboard'))
    return render_template('login.html', error=error)


@app.route("/dashboard",methods=('GET',))
#@login_required
def dashboard():
	return render_template("dashboard.html", username=session['username'])

@app.route("/create_user", methods=['GET', 'POST'])
def create_user():	
        conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
        cur = conn.cursor()
        
        if request.method == 'POST':
                name = request.form['name']
                password = request.form['password']
                role = request.form['role']
                cur.execute("SELECT username FROM users WHERE username='"+name+"';")
                results = cur.fetchall()
                if len(results) == 0:
                        cur.execute("SELECT role_pk FROM roles WHERE rolename='" + role + "';");
                        role_pk = cur.fetchall()
                        if len(role_pk) == 0:
                                cur.execute("INSERT INTO roles (rolename) VALUES ('"+role+"');")
                                cur.execute("SELECT role_pk FROM roles WHERE rolename='" + role + "';");
                                role_pk = cur.fetchall()
                        role_fk = role_pk[0]
                        cur.execute("INSERT INTO users (username, password, role_fk) VALUES ('"+name+"', '"+password+"', "+str(role_fk[0])+");")
                        conn.commit()
                        flash("User successfully inserted into database")
                else:
                        flash("User already has this name")
        conn.close()
        return render_template("create_user.html")

@app.route("/add_facility", methods=['GET', 'POST'])
def add_facility():
    conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
    cur = conn.cursor()
    
    cur.execute("SELECT common_name FROM facilities")
    facilities = cur.fetchall()

    if request.method == 'POST':
        name = request.form['name']
        code = request.form['code']
        cur.execute("SELECT common_name FROM facilities WHERE common_name='"+name+"';")
        results = cur.fetchall()
        if len(results) == 0:
            cur.execute("INSERT INTO facilities (common_name, code) VALUES ('"+name+"', '"+code+"');")
            conn.commit()
            flash("Facility successfully inserted into database")
        else:
            flash("Facility already in database")
    conn.close()
    return render_template("add_facility.html", facilities=facilities)


@app.route("/add_asset", methods=['GET', 'POST'])
def add_asset():
    conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
    cur = conn.cursor()
    cur.execute("SELECT common_name FROM facilities")
    facilities = cur.fetchall()
    cur.execute("SELECT asset_tag FROM assets")
    assets = cur.fetchall()
    if request.method == 'POST':
        asset_tag = request.form['asset_tag']
        description = request.form['description']
        facility = request.form['facility']
        date = request.form['date']
        cur.execute("SELECT asset_tag FROM assets WHERE asset_tag='"+asset_tag+"';")
        results = cur.fetchall()
        if len(results) == 0:
            cur.execute("INSERT INTO assets (asset_tag, description) VALUES ('"+asset_tag+"', '"+description+"');")
            cur.execute("SELECT asset_pk FROM assets WHERE asset_tag='"+asset_tag+"';")
            asset_pk = cur.fetchall()
            cur.execute("SELECT facility_pk FROM facilities WHERE common_name='"+facility+"';")
            facility_pk = cur.fetchall()
            facility_pk = facility_pk[0]
            asset_pk = asset_pk[0]
            cur.execute("INSERT INTO asset_at (asset_fk, facility_fk, arrive_dt) VALUES ("+str(asset_pk[0])+", "+str(facility_pk[0])+", '"+date+"');")
            conn.commit()
            flash("Asset successfully inserted into database")
        else:
            flash("Asset already in database")
    conn.close()
    return render_template("addAsset.html", facilities=facilities, assets=assets)


#@app.route("/login", methods=['GET', 'POST'])
#def login():
#    conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
#    cur = conn.cursor()
#	
#    error = ''
#    if request.method == 'POST':
#        cur.execute("SELECT password from users WHERE username='" + request.form['name'] + "';")
#        result = cur.fetchall()
#        if len(result) == 0:
#            error = "User doesn't exist"
#        else:
#            tmp = False
#            for password in result:
#                if password[0] == request.form['password']:
#                    tmp = True
#            if not tmp:
#                error = "Invalid password"
#            else:
#                session['name'] = request.form['name']
#                session['logged_in'] = True
#                session['role'] = 'test'
#                return redirect(url_for('dashboard'))
#	
#    return render_template('login.html', error=error)

@app.route("/dispose_asset", methods=['GET', 'POST'])
#@login_required
def disposeAsset():
    conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
    cur = conn.cursor()
    
    if session['role'] != 'officer':
        if request.method == 'POST':
            asset_tag = request.form['asset_tag']
            date = request.form['date']
            cur.execute("SELECT asset_pk FROM  assets WHERE asset_tag='"+asset_tag+"';")
            result = cur.fetchall()
            if len(result) == 0:
                flash("asset does not exist")
            else:
                asset_pk = result[0]
                cur.execute("UPDATE asset_at SET depart_dt='"+date+"' WHERE asset_fk="+str(asset_pk[0])+";")
                conn.commit()
                flash("asset_tag disposed")
                return redirect(url_for("dashboard"))
        conn.close()
        return render_template("disposeAsset.html")


    flash("Only logistics officers can dispose of assets")
    return render_template("main.html")

@app.route("/asset_report", methods=['GET', 'POST'])
#@login_required
def assetReport():
    data = ""
    conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
    cur = conn.cursor()
    cur.execute("SELECT common_name FROM facilities")
    facilities = cur.fetchall()

    if request.method == 'POST':
        facility = request.form['facility']
        date = request.form['date']
        try:
            cur.execute("SELECT asset_tag, common_name, arrive_dt FROM assets a JOIN asset_at aa ON asset_pk=asset_fk INNER JOIN facilities ON facility_fk=facility_pk WHERE facilities.common_name LIKE '%"+facility+"%' AND '"+date+"' >= aa.arrive_dt AND '"+date+"' <= aa.depart_dt;")
            data = cur.fetchall()
        except Exception as e:
            flash('Please enter a Date')
    conn.close()
    return render_template("assetReport.html", facilities=facilities, data=data)

@app.route("/logout")
#@login_required
def logout():
    session.clear()
    return redirect(url_for('main'))

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=8080, debug=True)
        

