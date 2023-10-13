from flask import Flask, render_template, redirect, url_for, request, json, session, flash, jsonify
from passlib.context import CryptContext
from flask_login import LoginManager, login_required, login_user, UserMixin, logout_user, current_user
import requests
import pandas as pd
import io
import traceback
import asyncio
import waitress
import MySQLdb
import bcrypt
from werkzeug.middleware.proxy_fix import ProxyFix
  
app = Flask(__name__, static_url_path='/NG999/static') 
login_manager = LoginManager(app)
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
app.secret_key = 'vfdjbfdkjvjdkfnvjkdfnvjkfdn'
app.config['API_URL'] = "http://ng999nginx/ng999Restapi"
PREFIX = "/NG999"
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

@app.route(f'{PREFIX}/login', methods=["GET", "POST"])
def login():
    try:
        if session is not None and 'reset_password_in_progress' in session and session['reset_password_in_progress'] == '1':
            try:
                password = request.form.get('passConfirmed')
                payload = {'user_id': session['user_id'], 'newPassword': password}
            
                url = app.config['API_URL'] + '/ng999/admin/resetPassword'
                response = requests.post(url, json=payload)
                
                if response.status_code == 200:
                    session.clear()
                    flash('Please Login with the new password')
                    return redirect(url_for('login'))
                
                session.clear()
                flash("Failed to reset password")
                return redirect(url_for('login'))
            
            except Exception as e:
                print(e, flush=True)
                session.clear()
                flash("Failed to reset password")
                return redirect(url_for('login'))
                
        else:

            if current_user.is_authenticated:
                return redirect(url_for('index'))
        
            if request.method == 'POST':
                username = request.form.get('username')
                password = request.form.get('password')
                
                url = app.config['API_URL'] + "/ng999/logon"
                data = { "username": username, "password": password }
                
                response = requests.post(url, json=data)
                
                if response.status_code == 200:
                    body = response.json()
                    
                    if body['role'] == '2' and body['isFirst'] == True:
                        session['reset_password_in_progress'] = '1'
                        session['user_id'] = body['user_id']
                        return render_template("resetPassword.html", userID=body['user_id'])

                    else:
                        user = User(body['username'])
                        login_user(user)
                        
                        session['user_id'] = body['user_id']
                        session['username'] = body['username']
                        session['role_id'] = body['role']
                        session['name'] = body['accountName']
                        session['isFirst'] = body['isFirst']
                    
                        flash('Login successful!', 'success')
                        return redirect(url_for('index'))
                
                else:
                    flash('Incorrect Credentials', 'danger')
                    return render_template("logon.html")
                
            return render_template('logon.html')
    
    except Exception as e:
        print(str(e), flush=True)
        return render_template("logon.html")

    
@app.route(f'{PREFIX}/logout')
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('login'))
        

@app.route(f"{PREFIX}/") 
@login_required
def index(): 
    try:
        if session['role_id'] == '1':
            
            finalList = {'wholeSaler': 0, 'active': 0, 'inactive': 0, 'totalCust': 0}
            
            url = app.config['API_URL'] + '/ng999/admin/dashboard'
            response = requests.get(url)
            
            if response.status_code == 200:
                finalList = response.json()
            
            return render_template("index.html", session=session, dashList=finalList) 
        
        url = app.config['API_URL'] + '/ng999/customer/getList'
        payload = {"wholesellerID": session['user_id'], "mode": "4"}
        
        response = requests.post(url, json=payload)
        
        body = {"active": 0, "totalUser": 0, "withMigrate": 0, "withoutMigrate": 0}
        
        if response.status_code == 200:
            body = response.json()
            
        return render_template("dashboardWholeseller.html", session=session, listCount=body)
    
    except Exception as e:
        flash(str(e))
        return redirect(url_for('logout'))
  
@app.route(f"{PREFIX}/createAccount")
@login_required
def accountCreate():
    try:
        if session['role_id'] != '1':
            flash("Unauthorized Access")
            return redirect(url_for('logout'))
        
        url = app.config['API_URL'] + "/ng999/company/list"
        response = requests.get(url)
        
        if response.status_code == 200:
            wholeSellerList = response.json()
            return render_template("account-create.html", wholesellerList=wholeSellerList, session=session)
            
    except Exception as e:
        print(e, flush=True)
        
@app.route(f"{PREFIX}/addAccount", methods=["POST"])
@login_required
def addAccount():
    try:
        if session['role_id'] != '1':
            flash("Unauthorized Access")
            return redirect(url_for('logout'))
        
        url= app.config['API_URL'] + "/ng999/account/add"
    
        name = request.form['name']
        role = request.form['role']
        email = request.form['email']
        wholesellerID = request.form['wholesellerID']
        
        body = {'name': name, 'role': role, 'email': email, 'wholesellerID': wholesellerID}
        
        response = requests.post(url, json=body)
        
        if response.status_code == 200:
            flash(f"Successfully created account for {name}")
            return redirect(url_for('accountCreate'))
        
        flash(f"Failed to create account for {name}")
        return redirect(url_for('accountCreate'))
    except Exception as e:
        print(e, flush=True)
        
@app.route(f"{PREFIX}/dataMigration", methods=["GET"])
@login_required
def dataMigration():
    try:
        custList = []
        if session['role_id'] != '2':
            flash("Unauthorized Access")
            return redirect(url_for('logout'))
        
        url = app.config['API_URL'] + '/ng999/customer/getList'
        payload = {"wholesellerID": session['user_id'], "mode": "3"}
        
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            custList = response.json()
        
        
        return render_template('dataMigration.html', session=session, customerList=custList)
        
    except Exception as e:
        print(e, flush=True)
        flash(str(e))
        return redirect(url_for('index'))
    
@app.route(f"{PREFIX}/withDeclaration", methods=["GET"])
@login_required
def withDeclaration():
    try:
        custList = []
        if session['role_id'] != '2':
            flash("Unauthorized Access")
            return redirect(url_for('logout'))
        
        url = app.config['API_URL'] + '/ng999/customer/getList'
        payload = {"wholesellerID": session['user_id'], "mode": "1"}
        
        response = requests.post(url, json=payload)
        
        
        if response.status_code == 200:
            custList = response.json()
        
        return render_template('withDeclaration.html', session=session, customerList=custList)
        
    except Exception as e:
        print(e, flush=True)
        flash(str(e))
        return redirect(url_for('index'))
    
    
@app.route(f"{PREFIX}/withoutDeclaration", methods=["GET"])
@login_required
def withoutDeclaration():
    try:
        if session['role_id'] != '2':
            flash("Unauthorized Access")
            return redirect(url_for('logout'))
        
        custList = []
        
        url = app.config['API_URL'] + '/ng999/customer/getList'
        payload = {"wholesellerID": session['user_id'], "mode": "2"}
        
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            custList = response.json()
        
        return render_template('withoutDeclaration.html', session=session, customerList=custList)
        
    except Exception as e:
        print(e, flush=True)
        flash(str(e))
        return redirect(url_for('index'))

@login_required
def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@login_required
def convert_to_string(value):
            if pd.notna(value):
                if isinstance(value, int):
                    return str(value).zfill(3)
                else:
                    return str(value)
            else:
                return ""
    
@app.route(f"{PREFIX}/uploadMigration", methods=['POST'])
@login_required
def uploadMigration():
    validExtension = ['xls', 'xlsx']
    
    if session['role_id'] != '2':
        flash("Unauthorized Access")
        return redirect(url_for('logout'))
    
    try:
        if 'file' not in request.files:
            raise Exception("No file found")
        
        file = request.files['file']
        
        if file.filename == '':
            raise Exception("Invalid File Name")
        if not allowed_file(file.filename, validExtension):
            raise Exception("Invalid File Extension")
        
        fileContent = file.read()
        df = pd.read_excel(io.BytesIO(fileContent), dtype={'CarllerNo': str})
        
        rows_list = []
        for index, row in df.iterrows():
            cleaned_row = {column: str(value) if pd.notna(value) else "" for column, value in row.items()}
            rows_list.append(cleaned_row)
        

        payload = {'data': rows_list, 'wholesellerID': session['user_id']}

        url = app.config['API_URL'] + "/ng999/customer/add"
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            flash("Uploaded migration list")
            return redirect(url_for('dataMigration'))
        
        flash("Fail to upload migration list")
        return redirect(url_for('dataMigration'))
        
    except Exception as e:
        print("Type:", type(e).__name__, flush=True)
        print("Message:", str(e), flush=True)
        print("Traceback:")
        traceback.print_exc()
        flash(str(e))
        return redirect(url_for('dataMigration'))
    
@app.route(f"{PREFIX}/accountList", methods=['GET'])
@login_required
def accountList():
    try:
        if session['role_id'] != '1':
            flash("Unauthorized Access")
            return redirect(url_for("logout"))
        
        url = app.config['API_URL'] + "/ng999/account/list"
        response = requests.get(url)
        
        body = []
    
        if response.status_code == 200:
            body = response.json()
        
        return render_template('accountList.html', WholesellerList=body, session=session)
        
    except Exception as e:
        flash(str(e))
        return redirect(url_for('index'))
    
@app.route(f"{PREFIX}/updateWhosellerPass", methods=["POST"])
@login_required
def adminResetPass():
    try:
        if session['role_id'] != '1':
            flash("Unauthorized Access")
            return redirect(url_for('logout'))
        
        password = request.form.get('confirmNewPass')
        accountID = request.form.get('accountID')
        
        payload = {'user_id': accountID, 'newPassword': password}
    
        url = app.config['API_URL'] + '/ng999/admin/resetPassword'
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            flash("Successfully reset password")
            return redirect(url_for("accountList"))
        
        flash("Failed to reset password")
        return redirect(url_for("accountList"))

        
    except Exception as e:
        print(e, flush=True)
        flash("Failed to reset password")
        return redirect(url_for("accountList"))
    

@app.route(f"{PREFIX}/companyList", methods=['GET'])
@login_required
def companyList():
    try:
        if session['role_id'] != '1':
            flash("Unauthorized Access")
            return redirect(url_for('logout'))
        
        url = app.config['API_URL'] + "/ng999/company/list"
        response = requests.get(url)
        
        cList = []
        
        if response.status_code == 200:
            cList = response.json()
        
        return render_template('createCompany.html', companyList=cList)
    
    except Exception as e:
        print(e, flush=True)
        flash(str(e))
        return redirect(url_for('index'))
    
@app.route(f"{PREFIX}/companyOperations", methods=["POST"])
@login_required
def companyOperations():
    try:
        if session['role_id'] != '1':
            flash("Unauthorized Access")
            return redirect(url_for('logout'))
        
        
        body = request.get_json()
        
        if body['mode'] == 1:
            url = app.config['API_URL'] + "/ng999/company/deleteCompany"
            payload = {"ID": body['ID']}
        
        else:
            url = app.config['API_URL'] + "/ng999/company/insertCompany"
            payload = {"Name": body['Name']}
                    
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            return jsonify({}), 200
        else:
            return jsonify({}), 404
            
        
    except Exception as e:
        print(e, flush=True)
        return jsonify({}), 404
    
@app.route(f"{PREFIX}/declare", methods=["POST"])
@login_required
def decalare():
    try:
        if session['role_id'] != '2':
            flash("Unauthorized Access")
            return redirect(url_for('logout'))
        
        body = {
            'CustID': str(request.form.get('modalcustID')),
            'Name': str(request.form.get('modalCustName')),
            'PhoneNo': str(request.form.get('modalCustPhone')),
            'Address': str(request.form.get('modalCustAddr')),
            'AdditionalInfo': str(request.form.get('modalCustInfo')),
            'WholeSellerID': session['user_id'],
            'bundle': "0"
        }
                        
        checkData = {key: str(value).replace(" ", "") for key, value in body.items()}
        
        if any(value == "" for value in checkData.values()):
            flash(f"Failed declaration at least one field is blank")
            return redirect(url_for("withoutDeclaration"))
            
        
        url = app.config['API_URL'] + "/ng999/company/declare"
        
        response = requests.post(url, json=body)
        
        if response.status_code == 200:
            flash(f"Success declaration for {body['Name']}")
            return redirect(request.referrer)
        
        flash(f"Fail declaration {response.json()['Message']}")
        return redirect(request.referrer)
    
    except Exception as e:
        flash(str(e))
        return redirect(request.referrer)
    
@app.route(f"{PREFIX}/bundleDeclare", methods=["GET"])
@login_required
def bundleDecalare():
    try:
        if session['role_id'] != '2':
            flash("Unauthorized Access")
            return redirect(url_for('logout'))
        
        custList = []
        
        url = app.config['API_URL'] + '/ng999/customer/getList'
        payload = {"wholesellerID": session['user_id'], "mode": "2"}
        
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            custList = response.json()
            
        return render_template("bundleDeclare.html", session=session, customerList=custList)
     
    except Exception as e:
        print(e, flush=True)
        flash(str(e))
        return render_template("bundleDeclare.html", session=session)
    
@app.route(f"{PREFIX}/bundleDeclarePost", methods=["POST"])
@login_required
def bundleDecalarePost():
    try:
        if session['role_id'] != '2':
            flash("Unauthorized Access")
            return redirect(url_for('logout'))
        
        body = request.get_json()
        url =  app.config['API_URL'] + '/ng999/customer/bundleDeclare'
        
        response = requests.post(url, json=body)
        
        if response.status_code == 200:
            return jsonify({}), 200
            
        return jsonify({}), 404

        
    except Exception as e:
        print(e, flush=True)
        flash(str(e))
        return jsonify({}), 404
    
if __name__ == '__main__':
	app.run(port=5000, threaded=True, use_reloader=True, debug=False)