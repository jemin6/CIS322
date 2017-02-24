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
            SQL = "SELECT * FROM users WHERE username=%s"
            cursor.execute(SQL,(user_name,))
            result = cursor.fetchone()
            print(result)
            if result:                     #if user name exist 
                session['error'] = 'Username <%s> is already taken.'%user_name
                return redirect('error')
            SQL= "INSERT INTO users (username,password) VALUES (%s,%s)"
            cursor.execute(SQL,(user_name,user_password))
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


#logout
@app.route('/logout')
def logout():
    return render_template('logout.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
