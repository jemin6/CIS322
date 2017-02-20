from flask import Flask, render_template, request, session, redirect, url_for
from config import dbname, dbhost, dbport, lost_priv, lost_pub, user_pub, prod_pub
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
        if(request.form['username'] and request.form['password']):
            session['logged_in'] = True
            session['username'] = request.form['username']
            return request.form['username'] + " Welcome."
        else:
            return 'Invaild username/password.'
    else:
        return 'Wrong access'

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')



@app.route('/create_user', methods=['POST','GET'])
def create_user():
    if request.method =='POST' and 'arguments' in request.form:
        req = json.loads(request.form['arguments'])

#    dat = dict()
#    dat['username'] = req['username']
#    dat['password'] = req['password']
#    data = json.dumps(dat)

#    SQL = "INSERT INTO users (username, password) VALUES (%s, %s)"
#    data1 = (req['username'],req['password'],)
#    cursor.execute(SQL,data1)
#    conn.commit()
#
#        if(request.form['username'] and request.form['password']):
#            session['logged_in'] = True
#            session['username'] = request.form['username']
#            return request.form['username'] + " is created"
#        else:
#            return 'Invaild username/password'
#    else:
#        return 'Wrong access'
#
    return render_template('create_user.html')

@app.route('/create_user_id',methods=['POST','GET'])
def create_user_id():
    return render_template('create_user_id.html')

#logout
@app.route('/logout')
def logout():
    return render_template('logout.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
