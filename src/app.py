from flask import Flask, render_template, request, session, redirect, url_for
from config import dbname,dbhost,dbport
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


#report filter screen 
@app.route('/report_filter_screen/')
def report_filter_screen():     
        return render_template('report_filter_screen.html')


#facility inventory report
@app.route('/facility_inventory_report', methods =['POST','GET'])
def facility_inventory_report():
#    if request.method == 'POST':
#        if 'facility_inventory_report' in request.form:
#            message = request.form['facility_inventory_report']
      SQL ="select * from assets"
      cursor.execute(SQL)
      result = cursor.fetchall()
      conn.commit()


#    con = sql.connect("database.db")
#    con.row_factory = sql.Row

#    cursor.con.cursor()
#    cursor.execute("select * from assets")
    
#    rows = cursor.fetchall();


#    if request.method == 'POST':
        #facility_inventory_report = request.form
      return render_template('facility_inventory_report.html')

@app.route('/in_transit_report')
def in_transit_report():
    return render_template('in_transit_report.html') 

@app.route('/logout')
def logout():
    return render_template('logout.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    
