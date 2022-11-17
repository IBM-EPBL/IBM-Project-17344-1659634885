from flask import Flask,render_template,request,redirect,url_for,session
import ibm_db
import re

app=Flask(__name__)
app.secret_keys='a'

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=0c77d6f2-5da9-48a9-81f8-86b520b87518.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31198;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=hbq98664;PWD=93R9nAZ3B709aixG",'','')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login',methods=['GET','POST'])
def login():
    global userid
    msg=" "
    
    if request.method=="POST":
        username = request.form['username']
        password = request.form['password']
        sql = "SELECT * FROM users WHERE username=? AND password=?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account  = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            session['Loggedin']=True
            session['id'] = account['USERNAME']
            userid = account["USERNAME"]
            session['username'] = account["USERNAME"]
            msg = 'Logged in Successfully!'
            return render_template("dashboard.html",msg=msg)
        else:
            msg = "Incorrect Username or Password"
    return render_template('Login.html',msg=msg)

@app.route("/register",methods=["GET","POST"])
def register():
    msg = " "
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        sql = "SELECT * FROM users WHERE username=?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = "Account already exists!"
        elif not re.match(r'[^@]+@[^@]+\.[^@]+',email):
            msg = "Invalid E-mail address"
        elif not re.match(r'[A-Za-z0-9]+',username):
            msg = "Name must contain only characters and numbers"
        else:
            insert_sql = "INSERT INTO users VALUES(?,?,?)"
            prep_stmt = ibm_db.prepare(conn,insert_sql)
            ibm_db.bind_param(prep_stmt,1,username)
            ibm_db.bind_param(prep_stmt,2,email)
            ibm_db.bind_param(prep_stmt,3,password)
            ibm_db.execute(prep_stmt)
            msg = "You have successfully Logged in!"
    
    elif request.method == "POST":
        msg = "Please fill out the form"
        return render_template('register.html')
    


    
if __name__ == '__main__':
   app.run(host='0.0.0.0',debug=(True))
            
        

