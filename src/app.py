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

def logged_user(func):                 #access allowed when logged in. 
    @wraps(func)
    def with_logging(*args, **kwargs):
        if 'logged_in' in session:
            return func(*args, **kwargs)
        else:
            flash("login required")
            return redirect(url_for('login_page'))
    return with_logging

# main page which is the beginning page
@app.route("/")
def main():
    return render_template("main.html", dbname=dbname, dbhost=dbhost, dbport=dbport)

# Login page for the users. Type vaild username and password to login
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
                if not temp:            # check if password is correct
                    error="Invalid password"
                else:
                    session['username'] = request.form['username']
                    session['logged_in'] =True
                    SQL="SELECT rolename FROM users JOIN roles ON users.role_fk=roles.role_pk WHERE users.username=%s"
                    cursor.execute(SQL,(session['username'],))
                    role=cursor.fetchone()
                    session['role'] = role[0]
                    return render_template('dashboard.html')
    return render_template('login.html', error=error)

# Dashboad page, which shows when login is successfully done
@app.route("/dashboard",methods=('GET',))
@logged_user
def dashboard():
    if session['role'] == 'Logistics Officer':
        SQL="SELECT * FROM requests WHERE request_pk NOT IN(SELECT request_fk FROM transit)"
        cursor.execute(SQL)
        data = cursor.fetchall()
        header = "Request"
        rows = ["Requester", "Request Date", "Source", "Destination"]
        url = "/approve_req"

    else:
        cursor.execute("SELECT * FROM transit WHERE load_time IS Null AND unload_time IS Null")
        data = cursor.fetchall()
        header = "Transit"
        rows = ["Request ID", "Load Time", "Unload Time"]
        url = "/update_transit"
        conn.commit()
    return render_template("dashboard.html",data=data, header=header, rows=rows, url=url)


# Create user screen where users can create username, password and the role. 
@app.route('/create_user',methods=['POST','GET'])
def create_user():
    if request.method=='GET':               # Load the create user page
        return render_template('create_user.html')
    if request.method=='POST':              # creates the user name & password 
        if 'username' in request.form and 'password' in request.form:
            user_name = request.form['username']
            user_password = request.form['password']
            role = request.form['rolename']
            SQL = "SELECT username FROM users WHERE username=%s"
            cursor.execute(SQL,(user_name,))
            result = cursor.fetchall()
            if len(result) == 0:
                SQL="SELECT role_pk FROM roles WHERE rolename=%s"
                cursor.execute(SQL,(role,))
                role_pk = cursor.fetchall()
                role_pk = role_pk[0][0]
                SQL= "INSERT INTO users (username,password,role_fk) VALUES (%s,%s,%s)"
                cursor.execute(SQL,(user_name,user_password,role_pk))
                conn.commit()
                # If username is created sucessfully, it pops up this message
                flash("##### REQUEST SUCCEED ######\n Username created!")
            else:
                # else, falses then pops up warning message
                flash("##### WARNING #####\n  Already taken username ")
    return render_template("create_user.html")

#Login required. Users adds facilities into the database
@app.route("/add_facility", methods=['GET', 'POST'])
@logged_user
def add_facility():
    cursor.execute("SELECT * FROM facilities ORDER BY common_name")
    session['facilities']=cursor.fetchall()
    if request.method=='POST':          # Insert new facility into the database
        if 'common_name' in request.form and 'fcode' in request.form:
            fcode = request.form['fcode']
            common_name = request.form['common_name']
            SQL="SELECT common_name FROM facilities WHERE common_name=%s OR fcode=%s"
            cursor.execute(SQL,(common_name,fcode))
            result = cursor.fetchall()
            if len(result) == 0:
                SQL="INSERT INTO facilities (common_name, fcode) VALUES (%s,%s)"
                cursor.execute(SQL,(common_name,fcode))
                conn.commit()
                flash("##### REQUEST SUCCEED ###### \nFacility successfully inserted into database!")
            else:
                flash("##### ERROR ###### \nFacility already in database!")
        return redirect(url_for('add_facility'))
    return render_template("add_facility.html")

#Add asset in to the datebase 
@app.route("/add_asset", methods=['GET', 'POST'])
def add_asset():
    cursor.execute("SELECT common_name FROM facilities")
    session['facilities'] = cursor.fetchall()
    cursor.execute("SELECT asset_tag, description FROM assets")
    session['assets'] = cursor.fetchall()
    if request.method == 'POST':
      if 'asset_tag' in request.form and 'description' in request.form and 'facility' in request.form and 'date' in request.form:
        asset_tag = request.form['asset_tag']
        description = request.form['description']
        facility = request.form['facility']
        date = request.form['date']
        SQL="SELECT asset_tag FROM assets WHERE asset_tag=%s"
        cursor.execute(SQL,(asset_tag,))
        result = cursor.fetchall()
        if len(result) == 0:
            SQL="INSERT INTO assets (asset_tag, description) VALUES (%s,%s)"
            cursor.execute(SQL,(asset_tag,description))
            SQL="SELECT asset_pk FROM assets WHERE asset_tag=%s"
            cursor.execute(SQL,(asset_tag,))
            asset_pk = cursor.fetchall()
            SQL="SELECT facility_pk FROM facilities WHERE common_name=%s"
            cursor.execute(SQL,(facility,))
            facility_pk = cursor.fetchall()
            facility_pk = facility_pk[0][0]
            asset_pk = asset_pk[0][0]
            SQL="INSERT INTO asset_at (asset_fk, facility_fk, arrive_dt) VALUES (%s,%s,%s)"
            cursor.execute(SQL,(asset_pk,facility_pk,date))
            conn.commit()
            flash("##### SUCCEED #####\n Asset successfully inserted")
        else:
            flash("##### WARNING #####\n Already existing data")
      return redirect(url_for('add_asset'))
    return render_template("add_asset.html")

# Disposing asset screen 
@app.route("/dispose_asset", methods=['GET', 'POST'])
@logged_user
def dispose_asset():
    if session['role'] == 'Logistics Officer':
        if request.method == 'POST':
            asset_tag = request.form['asset_tag']
            date = request.form['date']
            SQL="SELECT asset_pk FROM assets WHERE asset_tag=%s"
            cursor.execute(SQL,(asset_tag,))
            result = cursor.fetchall()
            if len(result) == 0:
                flash("##### WARNING #####\n Asset does not exist")
            else:
                asset_pk = result[0][0]
                SQL="SELECT disposed_dt FROM asset_at WHERE asset_fk=%s"
                cursor.execute(SQL,(asset_pk,))
                result = cursor.fetchall()
                print(result)
                if result[0][0]:
                    flash("##### WARNING #####\n Already been disposed")
                else:
                    SQL="UPDATE asset_at SET depart_dt=%s,disposed_dt=%s WHERE asset_fk=%s"
                    cursor.execute(SQL,(date,date,asset_pk))
                    conn.commit()
                    flash("##### SUCCEED ##### Asset tag disposed")
                return redirect(url_for("dispose_asset"))
        return render_template("dispose_asset.html")
    return redirect(url_for("not_logistic"))

#Major report for the application 
@app.route("/asset_report", methods=['GET', 'POST'])
@logged_user
def asset_report():
    cursor.execute("SELECT * FROM facilities ORDER BY common_name")
    session['facilities'] = cursor.fetchall()
    if request.method=='POST':
        facility = request.form['facility']
        date=request.form['date']
        SQL="SELECT asset_tag, description, common_name, arrive_dt, depart_dt FROM asset_at aa JOIN facilities f ON aa.facility_fk=f.facility_pk JOIN assets a ON a.asset_pk=aa.asset_fk WHERE (arrive_dt is null or arrive_dt<=%s) and (depart_dt is null or depart_dt>=%s)"
        cursor.execute(SQL,(date,date))
        session['data']=cursor.fetchall()
    return render_template("asset_report.html")

#Access controlled, only Logistics Officers should be able to initiate transfers
@app.route("/transfer_req", methods=['GET', 'POST'])
@logged_user
def transfer_req():
    cursor.execute("SELECT common_name FROM facilities;")
    facilities = cursor.fetchall()
    cursor.execute("SELECT asset_tag FROM assets;")
    assets = cursor.fetchall()
    if session['role'] == 'Logistics Officer':
        if request.method=='POST':
            asset_tag = request.form['asset_tag']
            source = request.form['source']
            destination = request.form['destination']
            date = request.form['date'] 
            SQL="SELECT asset_pk FROM assets WHERE asset_tag=%s"
            cursor.execute(SQL,(asset_tag,))
            asset_fk = cursor.fetchone()
            if asset_fk != None:
                SQL="SELECT user_pk from users WHERE username=%s"
                cursor.execute(SQL,(session,))
                user_pk = cursor.fetchone()
                SQL="SELECT facility_pk from facilities WHERE common_name=%s"
                cursor.execute(SQL,(source,))
                source_fk = cursor.fetchone()
                SQL="SELECT facility_pk from facilities WHERE common_name=%s"
                cursor.execute(SQL,(destination,))
                destination_fk = cursor.fetchone()
                SQL="INSERT INTO requests (requester_fk, request_dt, source_fk, destination_fk, assset_fk) VALUES (%s,%s,%s,%s,%s)"
                cursor.execute(SQL,(str(user_pk[0]),date,str(source_fk[0]),str(destination_fk[0]),str(asset_fk[0])))
                conn.commit()
                flash("##### REQUEST ##### Asset transfer success!")
                return redirect(url_for("dashboard"))
            flash( "##### WARNING ##### Asset Tag does NOT exist")
        return render_template("transfer_req.html",facilities=facilities, assets=assets)
    return redirect(url_for('not_logistic'))      #If the user is not a Logistics Officer

#Add transit requests, an interface is needed to approve/complete them
@app.route("/approve_req", methods=['GET', 'POST'])
@logged_user
def approve_req():
    if request.method=='GET':
        return render_template('approve_req.html' )
    if session['role'] == 'Facilities Officer':
        if request.method == 'POST':
            approval = request.form.getlist("approval")
            deny = request.form.getlist("deny")
            request_pk = request.form["request_pk"]
            if len(approval) != 0:
                flash("@@@ APPROVED @@@") 
                SQL="INSERT INTO transit (request_fk) VALUES (%s)"
                cursor.execute(SQL,(request_pk,))
            else:
                flash("Request has been removed")
                SQL="DELETE FROM requests WHERE request_pk=%s"
                cursor.execute(SQL,(request_pk,))
            conn.commit()
            return redirect(url_for("dashboard"))
        return render_template("approve_req.html", requests=requests)
    flash(" ** WARNING ** Only Facilities Officers can approve request")
    return redirect(url_for("dashboard"))

@app.route("/update_transit", methods=['GET', 'POST'])
def update_transit():
    if request.method=='GET':
        return render_template("update_transit.html")
    cursor.execute("SELECT * FROM transit WHERE load_time IS Null AND unload_time IS Null")
    transit = cursor.fetchall()
    if session['role'] == 'Logistics Officer':
        if request.method == 'POST':
            load_time = request.form['load']
            unload_time = request.form['unload']
            transit_pk = request.form["transit_pk"]
            SQL="UPDATE transit SET load_time=%s, unload_time=%s WHERE transit_pk=%s"
            cursor.execute(SQL,(load_time,unload_time,transit_pk))
            conn.commit()
            flash("Updated load/unload times")
            return redirect(url_for('dashboard'))
        return render_template("update_transit.html", transit=transit)
    flash(" ** WARNING ** Only Logistics Officer can update tracking information.")
    return redirect(url_for("login"))

#When user is not Logistic Officer
@app.route("/not_logistic")
def not_logistic():
    return render_template("not_logistic.html")

@app.route("/logout")
@logged_user
def logout():
    session.clear()
    return redirect(url_for('main'))

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=8080, debug=True)
        

