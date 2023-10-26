from flask import Flask, render_template, redirect, url_for, request, json, session, flash, jsonify, make_response
from passlib.context import CryptContext
from flask_login import LoginManager, login_required, login_user, UserMixin, logout_user, current_user
import requests
import pandas as pd
import io
import traceback
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Alignment
import asyncio
import waitress
import MySQLdb
import bcrypt
import re
from werkzeug.middleware.proxy_fix import ProxyFix
import img
  
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
    exempted_routes = ['login', 'forgetPassword', 'forgetPasswordPost']
    
    if not current_user.is_authenticated and request.endpoint not in exempted_routes:
        return redirect(url_for('login'))
    
@login_required
def validateEmail(email) -> bool:
    try:
        pattern = r'^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.com$'
        return bool(re.match(pattern, email))
    
    except Exception as e:
        print(e, flush=True)
        return False
    

@app.route(f'{PREFIX}/login', methods=["GET", "POST"])
def login():
    
    
    try:
        if session is not None and 'reset_password_in_progress' in session and session['reset_password_in_progress'] == '1':
            try:
                password = request.form.get('passConfirmed')
                payload = {'user_id': session['user_id'], 'newPassword': password, 'email': session['username']}
            
                url = app.config['API_URL'] + '/ng999/admin/resetPassword'
                response = requests.post(url, json=payload)
                
                if response.status_code == 200:
                    session.clear()
                    flash('Please Login with the new password')
                    return redirect(url_for('login'))
                
                session.clear()
                flash(response.json()['message'])
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
                        session['username'] = body['username']
                        return render_template("resetPassword.html", userID=body['user_id'], logonImg=img.base64Img)

                    else:
                        user = User(body['username'])
                        login_user(user)
                        
                        session['user_id'] = body['user_id']
                        session['username'] = body['username']
                        session['role_id'] = body['role']
                        session['name'] = body['accountName']
                        session['isFirst'] = body['isFirst']
                        
                        if session['role_id'] == '2':
                            session['compID'] = body['compID']
                            session['billingWholeSalerID'] = body['wID']
                            
                            session['companyName'] = body['cName'].lstrip()
                            session['companyName'] = session['companyName'].rstrip()
                            
                            
                        # print(session, flush=True)
                        
                        if session['role_id'] == '2' and not body['isActive']:
                            session.clear()
                            logout_user()
                            flash("Inactive User")
                            return redirect(url_for('login'))
                    
                        flash('Login successful!', 'success')
                        return redirect(url_for('index'))
                
                else:
                    flash('Incorrect Credentials', 'danger')
                    return render_template("logon.html", logonImg=img.base64Img)

            return render_template('logon.html', logonImg=img.base64Img)
    
    except Exception as e:
        print(str(e), flush=True)
        return render_template("logon.html", logonImg=img.base64Img)
    
@app.route(f'{PREFIX}/forgetPasswordPost', methods=['POST'])
def forgetPasswordPost():
    try:
        if session['forgetPassword'] != '1':
            return redirect(url_for('logout'))
        
        code = request.form.get('veri')
        password = request.form.get('passConfirmed')
        
        url = app.config['API_URL'] + "/ng999/admin/forgetPasswordReset"
        payload = {'email': session['email'], 'id': session['forgetID'], 'code': code, 'password': password}
        
        response = requests.post(url, json=payload)
        
        # print(response.json(), flush=True)
        
        if response.status_code == 200:
            flash('Please Login with the new password')
            session.clear
            return redirect(url_for('login'))
        
        flash(response.json()['message'])
        return redirect(url_for('logout'))
        
    except Exception as e:
        print(e, flush=True)
        flash("Unsuccessful password reset")
        return redirect(url_for('logout'))
    
        
    
@app.route(f'{PREFIX}/forgetPassword', methods=['GET', 'POST'])
def forgetPassword():
    try:
        if request.method == 'POST':
            email = request.form.get('email')
            
            if email.replace(" ", "") == '':
                flash('Invalid email')
                return redirect(url_for('logout'))
            
            payload = {'email': email}
            
            url = app.config['API_URL'] + "/ng999/admin/forgetPassword"
            
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                session['email'] = email
                session['forgetID'] = response.json()['id']
                
                return render_template('forgetPassVerification.html', session=session, logonImg=img.base64Img)
            
            flash('Invalid email')
            return redirect(url_for('logout'))
            
    
        else:
            session['forgetPassword'] = '1'
            return render_template('forgetPassword.html', session=session, logonImg=img.base64Img)
        
    except Exception as e:
        print(e, flush=True)
        return redirect(url_for('logout'))
            
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
        url2 = app.config['API_URL'] + '/ng999/account/getDashboardlist'
        recordList = []
        
        if session['role_id'] == '1':
            
            finalList = {'wholeSaler': 0, 'active': 0, 'inactive': 0, 'totalCust': 0}
            
            url = app.config['API_URL'] + '/ng999/admin/dashboard'
            response = requests.get(url)
            
            payload = {'mode': '1'}
            response2 = requests.post(url2, json=payload)
            
            if response.status_code == 200 and response2.status_code == 200:
                finalList = response.json()
                recordList = response2.json()
            
            # print(recordList, flush=True)
            return render_template("index.html", session=session, dashList=finalList, recordList=recordList, frameImg=img.frameImg) 
        
        url = app.config['API_URL'] + '/ng999/customer/getList'
        
        payload = {"wholesellerID": session['user_id'], "mode": "4", 'compID': session['compID']}
        payload2 = {'compID': session['compID'], 'mode': '2'}
        
        response = requests.post(url, json=payload)
        response2 = requests.post(url2, json=payload2)
        
        body = {"active": 0, "totalUser": 0, "withMigrate": 0, "withoutMigrate": 0}
        
        if response.status_code == 200 and response2.status_code == 200:
            body = response.json()
            recordList = response2.json()
        
        # print(recordList, flush=True)
        
        # print(body, flush=True)
        return render_template("dashboardWholeseller.html", session=session, listCount=body, recordList=recordList, frameImg=img.frameImg)
    
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
        
        flash("Fail to load wholeseller list")
        return render_template("account-create.html", wholesellerList=[], session=session)
            
    except Exception as e:
        print(e, flush=True)
        flash("Fail to load wholeseller list")
        return render_template("account-create.html", wholesellerList=[], session=session)
        
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
        
        if role == '2':
            wholesellerID = request.form['wholesellerID']
        else:
            wholesellerID = ""
            
        phoneNumber = request.form['pn']
        
        body = {'name': name, 'role': role, 'email': email, 'wholesellerID': wholesellerID, 'pn': phoneNumber}
        
        response = requests.post(url, json=body)
        
        if response.status_code == 200:
            flash(f"Successfully created account for {name}")
            return redirect(url_for('accountCreate'))
        
        flash(f"Failed to create account for {name} ({response.json()['message']})")
        return redirect(url_for('accountCreate'))
    
    except Exception as e:
        print(e, flush=True)
        flash("Fail create account")
        return render_template("account-create.html", wholesellerList=[], session=session)
        
@app.route(f"{PREFIX}/dataMigration", methods=["GET"])
@login_required
def dataMigration():
    try:
        if session['role_id'] != '2':
            flash("Unauthorized Access")
            return redirect(url_for('logout'))
        
        custList = []
        
        url = app.config['API_URL'] + '/ng999/customer/getList'
        payload = {"wholesellerID": session['user_id'], "mode": "3", 'compID': session['compID']}
        
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
        
        if session['role_id'] != '2':
            flash("Unauthorized Access")
            return redirect(url_for('logout'))
        
        custList = []
        
        url = app.config['API_URL'] + '/ng999/customer/getList'
        payload = {"wholesellerID": session['user_id'], "mode": "1", 'compID': session['compID']}
        
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
        payload = {"wholesellerID": session['user_id'], "mode": "2", 'compID': session['compID']}
        
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            custList = response.json()
        
        return render_template('withoutDeclaration.html', session=session, customerList=custList)
        
    except Exception as e:
        print(e, flush=True)
        flash(str(e))
        return redirect(url_for('index'))
    
@app.route(f"{PREFIX}/fullList", methods=["GET"])
@login_required
def fullList():
    try:
        if session['role_id'] != '2':
            flash("Unauthorized Access")
            return redirect(url_for('logout'))
        
        custList = []
        
        url = app.config['API_URL'] + '/ng999/customer/getList'
        payload = {"wholesellerID": session['user_id'], "mode": "5", 'compID': session['compID']}
        
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            custList = response.json()
            
        # print(custList, flush=True)
        
        return render_template('allMigration.html', session=session, customerList=custList)
        
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
    if session['role_id'] != '2':
        flash("Unauthorized Access")
        return redirect(url_for('logout'))
    
    validExtension = ['xls', 'xlsx']
    
    try:
        if 'file' not in request.files:
            raise Exception("No file found")
        
        file = request.files['file']
        
        if file.filename == '':
            raise Exception("Invalid File Name")
        
        if not allowed_file(file.filename, validExtension):
            raise Exception("Invalid File Extension")
        
        fileContent = file.read()
        df = pd.read_excel(io.BytesIO(fileContent), dtype={'CallerNo': str})
        
        rows_list = []
        for index, row in df.iterrows():
            cleaned_row = {column: str(value) if pd.notna(value) else "" for column, value in row.items()}
            rows_list.append(cleaned_row)
        

        payload = {'data': rows_list, 'wholesellerID': session['user_id'], 'compID': session['compID'], 
                   'accountID': session['user_id']}

        url = app.config['API_URL'] + "/ng999/customer/add"
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            message = response.json()
            flash(message['message'])
            return redirect(url_for('dataMigration'))
        
        
        # print(response.json(), flush=True)
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
        
        payload = {'user_id': accountID, 'newPassword': password, 'email': session['username']}
    
        url = app.config['API_URL'] + '/ng999/admin/resetPassword'
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            flash("Successfully reset password")
            return redirect(url_for("accountList"))
        
        flash(response.json()['message'])
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
            return jsonify({}), 400
            
        
    except Exception as e:
        print(e, flush=True)
        return jsonify({}), 400
    
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
        
        # print(body, flush=True)
                        
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
    
@app.route(f"{PREFIX}/bundleDeclare/<mode>", methods=["GET"])
@login_required
def bundleDecalare(mode):
    try:
        if session['role_id'] != '2':
            flash("Unauthorized Access")
            return redirect(url_for('logout'))
        
        custList = []
        
        url = app.config['API_URL'] + '/ng999/customer/getList'
        payload = {"wholesellerID": session['user_id'], "mode": "2", 'compID': session['compID']}
        
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            custList = response.json()
        
        if str(mode) == "1":
            flash("Successful bundle declare")
            
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
            
        return jsonify({}), 400

    except Exception as e:
        print(e, flush=True)
        flash(str(e))
        return jsonify({}), 400
    
@app.route(f"{PREFIX}/downloadExcel", methods=['POST'])
@login_required
def downloadExcel():
    try:
        
        if session['role_id'] != '2':
            return jsonify({}), 400
        
        resultList = []
        
        url = app.config['API_URL'] + '/ng999/customer/getWholeSalerCust'
        payload = {'wholeSalerID': session['billingWholeSalerID']}
        # print(payload, flush=True)
        
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            # print(response.json(), flush=True)
            resultList = response.json()
        
        workbook = Workbook()
        
        sheet = workbook.active
        sheet.title = "Migration Template"
        
        header = ["CustID", "Name", "Address", "Address1", "Address2", "Address3", "CallerNo"]
        sheet.append(header)
        
        
        for data in resultList:
            rowData = [data.get(column_name, "") for column_name in header]
            sheet.append(rowData)
        
        
        # for column_cells in sheet.columns:
        #     length = max(len(str(cell.value)) for cell in column_cells)
        #     col_letter = column_cells[0].column_letter
        #     sheet.column_dimensions[col_letter].width = length + 2
            
        #     for cell in column_cells:
        #         cell.alignment = Alignment(horizontal="left", vertical="center")
        
        
        excel_file = io.BytesIO()
        workbook.save(excel_file)
        excel_file.seek(0)

        response = make_response(excel_file.read())
        response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response.status_code = 200
        
        return response
        
    except Exception as e:
        print(e, flush=True)
        return jsonify({}), 400
    
@app.route(f"{PREFIX}/updateInfo", methods=['POST'])
def updateInfo():
    try:
        if session['role_id'] != '1':
            flash("Unauthorized Access")
            return redirect(url_for('logout'))
        
        if not validateEmail(str(request.form.get('accEmail'))):
            flash("Invalid email format")
            return redirect(request.referrer)
            
        body = {
                'accID': str(request.form.get('accInfoID')),
                'name': str(request.form.get('accName')),
                'PhoneNo': str(request.form.get('accPn')),
                'email': str(request.form.get('accEmail')),
                'status': request.form.get('accStatus') is not None
            }
        
        # print(body, flush=True)
        
        url = app.config['API_URL'] + '/ng999/account/updateInfo'
        
        response = requests.post(url, json=body)
        
        if response.status_code == 200:
            flash(f"Updated Account Info for {body['name']}")
            return redirect(request.referrer)
            
        flash("Fail to update account info")
        return redirect(request.referrer)
        
    except Exception as e:
        flash("Fail to update account info")
        return redirect(request.referrer)
    
    
if __name__ == '__main__':
	app.run(port=5000, threaded=True, use_reloader=True, debug=False)