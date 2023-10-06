from flask import Flask, render_template, redirect, url_for, request, json, session, flash
from passlib.context import CryptContext
from flask_login import LoginManager, login_required, login_user, UserMixin, logout_user, current_user
import requests
import asyncio
import waitress
import MySQLdb
  
app = Flask(__name__) 
login_manager = LoginManager(app)
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
app.secret_key = 'vfdjbfdkjvjdkfnvjkdfnvjkfdn'

class User:
    def __init__(self, email):
        self.user_id = email

    def get_id(self):
        return str(self.user_id)

    @property
    def is_authenticated(self):
        return True 

    @property
    def is_anonymous(self):
        return False

    @property
    def is_active(self):
        return True
        
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.before_request
def check_authentication():
    if not current_user.is_authenticated and request.endpoint != 'login':
        return redirect(url_for('login'))

@app.route('/login', methods=["GET", "POST"])
def login():
    try:
        if current_user.is_authenticated:
            return redirect(url_for('index'))
    
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            url = "http://localhost:8888/ng999/logon"
            data = { "username": username, "password": password}
            
            response = requests.post(url, json=data)
            
            if response.status_code == 200:
                body = response.json()
                
                user = User(body['username'])
                login_user(user)
                
                session['user_id'] = body['user_id']
                session['username'] = body['username']
                session['role_id'] = body['role']
                session['name'] = body['accountName']
                                
                flash('Login successful!', 'success')
                return redirect(url_for('index'))
            
            else:
                flash('Incorrect Credentials', 'danger')
                return render_template("logon.html")
            
        flash('Incorrect Credentials', 'danger')
        return render_template('logon.html')
    
    except Exception as e:
        print(e)
        return render_template("logon.html")
    
    
@app.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('login'))
        

@app.route("/") 
@login_required
async def index(): 
    if session['role_id'] == '1':
        return render_template("index.html", session=session) 
    
    return render_template("dashboardWholeseller.html", session=session)

async def hello():
    return "x"
  
@app.route("/createAccount")
@login_required
def accountCreate():
    try:
        url = "http://localhost:8888/ng999/company/list"
        response = requests.get(url)
        
        if response.status_code == 200:
            wholeSellerList = response.json()
            return render_template("account-create.html", wholesellerList=wholeSellerList)
            
    except Exception as e:
        print(e)
        
@app.route("/addAccount", methods=["POST"])
def addAccount():
    try:
        url= "http://localhost:8888/ng999/account/add"
    
        name = request.form['name']
        role = request.form['role']
        email = request.form['email']
        wholesellerID = request.form['wholesellerID']
        
        body = {'name': name, 'role': role, 'email': email, 'wholesellerID': wholesellerID}
        
        response = requests.post(url, json=body)
        
        if response.status_code == 200:
            return redirect(url_for('index'))
    
    except Exception as e:
        print(e)
        
@app.route("/dataMigration", methods=["GET"])
@login_required
def dataMigration():
    try:
        if session['role_id'] != '2':
            return redirect(url_for('logout'))
        
        
        
        return render_template('dataMigration.html', session=session)
        
    except Exception as e:
        print(e)
        return redirect(url_for('index'))
    

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=9032, threaded=True, use_reloader=True,debug=False)