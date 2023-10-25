from fastapi import FastAPI, APIRouter, Depends, HTTPException, Request
from httpx import AsyncClient
import uvicorn
from typing import Any, Dict, AnyStr, List, Union,Annotated
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from datetime import date, datetime
from pydantic import BaseModel
import bcrypt
from passlib.context import CryptContext
import secrets
import string
import MySQLdb
import traceback
import re
import pymssql
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
data = []

class mailSetting():
    port = 587
    smtp_server = "mail.redtone.com"
    sender_email = "frim@biz.redtone.com"
    password = '6elk@hkU'
    theme = "NG999 System Notification"
    sender = "noreply@ng999.redtone.com"
    cc = "yungsheng.ho@redtone.com"

    
def generate_password(length=12) -> str:
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))
    
    return password

async def validateEmail(email) -> bool:
    try:
        pattern = r'^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.com$'
        return bool(re.match(pattern, email))
    
    except Exception as e:
        print(e, flush=True)
        return False

async def checkEmail(email, accountID=None) -> bool:
    conn_ng999 = await getSqlCONN()
    cursor = conn_ng999.cursor()
    
    if accountID is None:
        query = """

        select * from Account where Account_Email = %s
        
        """
        values = (email, )
    else:
        
        query = """

        select * from Account where Account_Email = %s and Account_ID != %s
        
        """
        values = (email, accountID)
        
    cursor.execute(query, values)
    
    result = cursor.fetchone()
    
    if result is not None and len(list(result)) > 0:
        await closeConn(cursor, conn_ng999)
        return True
    
    await closeConn(cursor, conn_ng999)
    return False

async def checkPhoneNumber(phoneNumber, accID=None) -> bool:
    conn_ng999 = await getSqlCONN()
    cursor = conn_ng999.cursor()
    
    if accID is None:
    

        query = """

        select * from Account where Account_Phone_Number = %s
        
        """
        values = (phoneNumber, )
    else:
        
        query = """

        select * from Account where Account_Phone_Number = %s and Account_ID != %s
        
        """
        values = (phoneNumber,accID)
        
   
    cursor.execute(query, values)
    
    result = cursor.fetchone()
    
    if result is not None and len(list(result)) > 0:
        await closeConn(cursor, conn_ng999)
        return True
    
    await closeConn(cursor, conn_ng999)
    return False
    
@app.post("/ng999/account/add")
async def add_ng999_company_data(request: Request):
    password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    try:
        body = await request.json()
        
        if await checkEmail(body['email']) or await checkPhoneNumber(body['pn']):
            return JSONResponse(content={'message': 'Duplicate email/phone number'}, status_code=400)
        
        if not await validateEmail(body['email']):
            return JSONResponse(content={'message': 'Invalid email format'}, status_code=400)
            
        
        conn_ng999 = await getSqlCONN()
        cursor = conn_ng999.cursor()
        conn_ng999.begin()
        
        # Will use it later 
        # password = generate_password()
        password = "P@ssw0rd2288"
        
        hashPassword = password_context.hash(password)
        
        query = """
            
            insert into Account (Account_Password, Account_name, Account_Role, Account_date_Created, Account_Email, Account_Phone_Number, lastActive) 
            values (%s, %s, %s, %s, %s, %s, %s)
            
            """
            
        values = (hashPassword, body['name'], body['role'], datetime.now(), body['email'], body['pn'], datetime.now())
        
        if body['role'] == '2':
            query = """
            
            insert into Account (Account_Password, Account_name, Account_Role, Account_date_Created, Company_ID, Account_Email, isFirst, isActive, Account_Phone_Number, lastActive) 
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            
            
            """
            
            values = (hashPassword, body['name'], body['role'], datetime.now(), body['wholesellerID'], body['email'], True, False, body['pn'], datetime.now())
        
        cursor.execute(query, values)
        
        if cursor.rowcount > 0:
            conn_ng999.commit()
            
            await closeConn(cursor, conn_ng999)
            await sendEmail(body['email'], password, '1')
            return JSONResponse(content={}, status_code=200)
        
        await closeConn(cursor, conn_ng999)
        return JSONResponse(content={"message": "Uncatched Error"}, status_code=400)
    
    except Exception as e:
        print(e, flush=True)
        await closeConnRollback(cursor, conn_ng999)
        return JSONResponse(content={"Message": str(e)}, status_code=400)
    
@app.post('/ng999/admin/resetPassword')
async def resetPassword(request:Request):
    try:
        password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        body = await request.json()
        
        conn_ng999 = await getSqlCONN()
        cursor = conn_ng999.cursor()
        conn_ng999.begin()
        
        password = body['newPassword']
        
        hashPassword = password_context.hash(password)
        
        query = """
        
        update Account set Account_Password = %s, isFirst = %s, isActive = %s, lastActive = %s where Account_ID = %s
        
        """
        
        values = (hashPassword, False, True, datetime.now(), body['user_id'])
        
        cursor.execute(query, values)
        
        if cursor.rowcount > 0:
            conn_ng999.commit()
            
            await closeConn(cursor, conn_ng999)
            await sendEmail(body['email'], password, '0')
            
            return JSONResponse(content={}, status_code=200)
            
        await closeConn(cursor, conn_ng999)
        return JSONResponse(content={}, status_code=400)
        
    except Exception as e:
        print(e, flush=True)
        await closeConnRollback(cursor, conn_ng999)
        return JSONResponse(content={}, status_code=400)
    
async def sendEmail(to, password, isCreate):
    try:
        content = await generateEmailContent(to, password, isCreate)
        # print(content, flush=True)
        # print(to, flush=True)
        
        # url = "http://172.31.0.1:8888/email/add"
        url = "https://apis.redtone.com:9999/email/add"
        payload = {
                    "to_list": to,
                    "cc": "",
                    "bcc": "yungsheng.ho@redtone.com",
                    "subject": content[0],
                    "body": content[1],
                    "url": "",
                    "url_title": "",
                    "ishtml": 1,
                    "template": 1
                    }
        
        async with AsyncClient() as client:
            response = await client.post(url, json=payload)
            
            # print(response.json(), flush=True)
            
            if response.status_code == 200:
                # url = "http://172.31.0.1:8888/email/send"
                url = "https://apis.redtone.com:9999/email/send"
                response = await client.get(url)
                # print(response, flush=True)
            
        # server = smtplib.SMTP(mailSetting.smtp_server, mailSetting.port)
        # msg = MIMEMultipart()
        # msg['From'] = mailSetting.sender
        # msg['To'] = to
        # msg['Cc'] = mailSetting.cc
        
        # content = await generateEmailContent(to, password, isCreate)
        
        # msg['Subject'] = content[0]
        # msg.attach(MIMEText(content[1], 'html'))

        # server.starttls()
        # server.login(mailSetting.sender_email, mailSetting.password)
        # server.sendmail(mailSetting.sender_email, [mailSetting.to, mailSetting.cc], msg.as_string())
        # server.quit()
    except Exception as e:
        print(e, flush=True)
        
async def generateEmailContent(email, newPassword, isCreate):
    try:
        email_subject = "NG999 System Notification"

        email_template = """
        <html>
        <head></head>
        <body>
            <p>Hi,</p>
            <p>{mode}</p>
            <ul>
                <li><strong>Username:</strong> {username}</li>
                <li><strong>New Password:</strong> {pwd}</li>
            </ul>
            <p>Make sure to keep your login details secure.{isReset}</p>
            <p>Thank you for using our service.</p>
            <p>Sincerely,</p>
            <p>Your Support Team</p>
        </body>
        </html>
        """
        
        modeTitle = 'Your password has been reset. Here are your new login details:'
        resetBody = ' If you did not request this password reset, please contact our support team immediately.'
        
        if isCreate == '1':
            modeTitle = 'Your account has been created successfully. Here are your default login details:'
            resetBody = ""
            
        email_content = email_template.format(pwd=newPassword, mode=modeTitle, username=email, isReset=resetBody)

        return email_subject, email_content
        
    except Exception as e:
        print(e, flush=True)



@app.post("/ng999/logon")
async def ng999_logon(request:Request):
    try:
        password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        body = await request.json()
        
        conn_ng999 = await getSqlCONN()
        cursor = conn_ng999.cursor()
        
        query = "select account_password, account_role, account_email, account_id, account_name, isFirst, isActive, Account.Company_ID, Company.wholeSalerID, Company.Company_Name from Account left join Company on Account.Company_ID = Company.Company_ID where account_email = %s"
        
        values = (body['username'],)
        cursor.execute(query, values)
        result = cursor.fetchone()
                        
        if result:
            if list(result)[0] is not None:                
                if password_context.verify(body['password'], list(result)[0]):
                    await closeConn(cursor, conn_ng999)
                    compID = ""
                    wholeSalerID = ""
                    cName = ""
                    
                    if list(result)[1] == '2':
                        compID = list(result)[7]
                        wholeSalerID = list(result)[8]
                        cName = list(result)[9]
                        
                    return JSONResponse(content={'user_id': list(result)[3], 'username': list(result)[2], 'role': list(result)[1], 'accountName': list(result)[4], 'isFirst': list(result)[5], 'isActive': list(result)[6], 'compID': compID, 'wID': wholeSalerID, 'cName': cName}, status_code=200)
        
        await closeConn(cursor, conn_ng999)
        return JSONResponse(content={'Message': "Incorrect Password"}, status_code=400)
                
    except Exception as e:
        print(e, flush=True)
        await closeConn(cursor, conn_ng999)
        return JSONResponse(content={}, status_code=400)

# Route to delete an item
@app.delete("/ng999/company/delete/{id}")
async def delete_ng999_company_data(Company_ID: int):
    try:
        conn_ng999 = await getSqlCONN()
        cursor = conn_ng999.cursor()
        conn_ng999.begin()
        
        query = "DELETE FROM Company WHERE Company_ID=%s"
        cursor.execute(query, (Company_ID,))
        
        conn_ng999.commit()
        await closeConn(cursor, conn_ng999)
        
        return {"Company_ID": Company_ID}
    
    except Exception as e:
        print(e, flush=True)
        await closeConnRollback(cursor, conn_ng999)
        return JSONResponse(content={}, status_code=400)
   

@app.get("/ng999/company/list")
async def get_ng999_company_datas():
    try:
        conn_ng999 = await getSqlCONN()
        cursor = conn_ng999.cursor()
        
        query = "SELECT * FROM Company where Company_ID"
        cursor.execute(query)
        item = cursor.fetchall()
        
        columnnName = [desc[0] for desc in cursor.description]
        resultDict = []
        
        if item is None:
            raise HTTPException(status_code=400, detail="Data not found")
        
        for row in list(item):
            rowDict = {}
            for i, col_name in enumerate(columnnName):
                rowDict[col_name] = str(row[i])
            
            resultDict.append(rowDict)
            
        await closeConn(cursor, conn_ng999)
        return resultDict
    
    except Exception as e:
        print(e, flush=True)
        await closeConn(cursor, conn_ng999)
        return JSONResponse(content={}, status_code=400)
    
@app.get("/ng999/account/list")
async def getAccountList():
    try:
        conn_ng999 = await getSqlCONN()
        cursor = conn_ng999.cursor()
        
        query = "SELECT * FROM Account a join Company c on a.company_id = c.company_id where a.Account_Role = '2'"
        cursor.execute(query)
        item = cursor.fetchall()
        
        columnnName = [desc[0] for desc in cursor.description]
        resultDict = []
        
        if item is None:
            raise HTTPException(status_code=400, detail="Data not found")
        
        for row in list(item):
            rowDict = {}
            for i, col_name in enumerate(columnnName):
                if col_name == 'lastActive':
                        try:
                            dateObject = datetime.strptime(str(row[i]), "%Y-%m-%d %H:%M:%S")
                            formattedDate = dateObject.strftime("%d/%m/%Y %H:%M:%S")
                            rowDict[col_name] = str(formattedDate)
                        except Exception as e:
                            rowDict[col_name] = str(row[i])
                else:
                    rowDict[col_name] = str(row[i])
                    
                # rowDict[col_name] = str(row[i])
            
            resultDict.append(rowDict)
            
        await closeConn(cursor, conn_ng999)
        return resultDict
    
    except Exception as e:
        print(e, flush=True)
        await closeConn(cursor, conn_ng999)
        return JSONResponse(content={}, status_code=400)
    
async def checkCustDB(accountID, phoneNumber) -> bool:
    try:
        conn_ng999 = await getSqlCONN()
        cursor = conn_ng999.cursor()
        
        # query = """
    
        # select * from Customer where account_id = %s and Customer_Phone_Number = %s
        # """
        
        query = """
    
        select * from Customer where Customer_Phone_Number = %s
        """
        
        values = (phoneNumber,)
        cursor.execute(query, values)
        
        result = cursor.fetchone()
        
        if result and len(list(result)) > 0:
            await closeConn(cursor, conn_ng999)
            return True 
        
        await closeConn(cursor, conn_ng999)
        return False
    
    except Exception as e:
        print(e, flush=True)
        await closeConn(cursor, conn_ng999)
        return False
    
async def checkCustDBDeclare(custID, phoneNumber) -> bool:
    try:
        conn_ng999 = await getSqlCONN()
        cursor = conn_ng999.cursor()
        
        query = """
    
        select * from Customer where Customer_ID != %s and Customer_Phone_Number = %s
        """
        
        values = (custID, phoneNumber)
        cursor.execute(query, values)
        
        result = cursor.fetchone()
        
        if result and len(list(result)) > 0:
            await closeConn(cursor, conn_ng999)
            return True 
        
        await closeConn(cursor, conn_ng999)
        return False
    
    except Exception as e:
        print(e, flush=True)
        await closeConn(cursor, conn_ng999)
        return False
    
    
@app.post("/ng999/customer/add")
async def get_ng999_company_datas(request:Request):
    try:
        body = await request.json()
    
        conn_ng999 = await getSqlCONN()
        cursor = conn_ng999.cursor()
        conn_ng999.begin()
        insertedCount: int = 0
        duplicatedPhoneNumber: int = 0
        emptyPhoneNumber: int = 0
        emptyAddress: int = 0
        emptyName: int = 0
        
        for i in body['data']:
            # No duplicated phone number can be inserted to the db
            address = i['Address'] + " " + i['Address1'] + " " + i['Address2'] + " " + i['Address3']
            
            if i['CallerNo'].replace(" ", "") == "":
                emptyPhoneNumber += 1
                continue
            
            if i['Name'].replace(" ", "") == "":
                emptyName += 1
                continue
            
            if address.replace(" ", "") == "":
                emptyAddress += 1
                continue
                
            if await checkCustDB(body['wholesellerID'], i['CallerNo']):
                duplicatedPhoneNumber += 1
                continue
            
            insertedCount += 1
            
            query = """
            
            Insert into Customer (Customer_Name, Customer_Migration_Date,
            Customer_Address, Customer_Phone_Number, Customer_Additional_Info, Account_ID, CustBillingID) 
            values (%s, %s, %s, %s, %s, %s, %s);
    
            """
            values = (i['Name'], datetime.now(), i['Address'] + " " + i['Address1'] + " " + i['Address2'] + " " + i['Address3'], i['CallerNo'], i['WholeSaleID'], body['wholesellerID'], i['CustID'])

            cursor.execute(query, values)
            
            
        uploadedCount = insertedCount
        
        query = """
        
        Insert into Log_Record (Log_Date, Log_Record_No, Account_ID, Log_Company_ID)
        values (%s, %s, %s, %s)
        """
        
        values= (datetime.now(), uploadedCount, body['accountID'], body['compID'])
        cursor.execute(query, values)
        conn_ng999.commit()
        
        await closeConn(cursor, conn_ng999)
        return JSONResponse(content={'message': f"Uploaded {str(uploadedCount)} records. Duplicate Phone Number {str(duplicatedPhoneNumber)}. Empty Name {str(emptyName)}. Empty Phone Number {str(emptyPhoneNumber)}. Empty Addess {str(emptyAddress)}."}, status_code=200)
        
        
    except Exception as e:
        print("Type:", type(e).__name__, flush=True)
        print("Message:", str(e), flush=True)
        print("Traceback:")
        traceback.print_exc()
        
        await closeConnRollback(cursor, conn_ng999)
        return JSONResponse(content={"message": str(e)}, status_code=400)
    
@app.post('/ng999/account/getDashboardlist')
async def getDashboardList(request:Request):
    try:
        returnDict = []
        body = await request.json()
        
        conn_ng999 = await getSqlCONN()
        cursor = conn_ng999.cursor()
        
        if body['mode'] == '1':
            query = """
            
            SELECT a.Account_Name, c.Company_Name, l.Log_Date, l.Log_Record_No 
            FROM Log_Record l join Company c on l.Log_Company_ID = c.Company_ID 
            join Account a on a.Account_ID = l.Account_ID;
            
            """
            cursor.execute(query)
            
        else:
        
            query = """
            
            SELECT a.Account_Name, c.Company_Name, l.Log_Date, l.Log_Record_No 
            FROM Log_Record l join Company c on l.Log_Company_ID = c.Company_ID 
            join Account a on a.Account_ID = l.Account_ID 
            where l.Log_Company_ID = %s;
            """
            values = (body['compID'],)
            cursor.execute(query, values)

        result = cursor.fetchall()
        
        if result is not None and len(list(result)):
            for row in list(result):
                tempDict = {}
                
                try:
                    dateObject = datetime.strptime(str(row[2]), "%Y-%m-%d %H:%M:%S")
                    formattedDate = dateObject.strftime("%d/%m/%Y %H:%M:%S")
                    tempDict['date']= str(formattedDate)
                    
                except Exception as e:
                    tempDict['date'] = str(row[2])
                    
                tempDict['recordNo'] = str(row[3])
                tempDict['accountName'] = str(row[0])
                tempDict['companyName'] = str(row[1])
                
                returnDict.append(tempDict)
                
        await closeConn(cursor, conn_ng999)
        return JSONResponse(content=returnDict, status_code=200)
    
    except Exception as e:
        print(e, flush=True)
        await closeConn(cursor, conn_ng999)
        return JSONResponse(content=[], status_code=400)
        
    
    
async def getCount(wholesellerID, companyID=None) -> dict:
    try:
        body = {"active": 0, "totalUser": 0, "withMigrate": 0, "withoutMigrate": 0}
        
        conn_ng999 = await getSqlCONN()
        cursor = conn_ng999.cursor()
        
        queryList = ["""
        select count(*) from Customer where Account_ID = %s
        """,
        """
        select count(*) from Customer where Account_ID = %s and customer_declaration_date is not null
        
        """,
        """
        select count(*) from Customer where Account_ID = %s and customer_declaration_date is null
        """,
        """
        select count(*) from Account where isActive = True and Company_ID = %s;
        """
        ]
        
        for index, q in enumerate(queryList):
            
            # values = (wholesellerID, )
            # cursor.execute(q, values)
            
            if index < 3:
                values = (wholesellerID, )
                cursor.execute(q, values)
            else:
                values = (companyID, )
                cursor.execute(q, values)
            
            result = cursor.fetchone()
            
            if result and len(list(result)) > 0:
                
                if index == 0:
                    body['totalUser'] = list(result)[0]
                elif index == 1:
                    body['withMigrate'] = list(result)[0]
                elif index == 2:
                    body['withoutMigrate'] = list(result)[0]
                else:
                    body['active'] = list(result)[0]
                    
        
        await closeConn(cursor, conn_ng999)
        return body
    
    except Exception as e:
        print(e, flush=True)
        await closeConn(cursor, conn_ng999)
        return {"active": 0, "totalUser": 0, "withMigrate": 0, "withoutMigrate": 0}
                

@app.post("/ng999/customer/getList")
async def get_ng999_company_datas(request:Request):
    try:
        body = await request.json()
        
        conn_ng999 = await getSqlCONN()
        cursor = conn_ng999.cursor()
        
        resultDict = []
        
        query = """
        
        SELECT * FROM Customer c join Account a on c.Account_ID = a.Account_ID where a.Company_ID = %s and date(c.customer_migration_date) = curdate()
        
        """
        
        if body['mode'] == "1":
            query = """
            SELECT * FROM Customer c join Account a on c.Account_ID = a.Account_ID where a.Company_ID = %s and c.customer_declaration_date is not null
            """
        elif body['mode'] == "2":
            query = """
            
            SELECT * FROM Customer c join Account a on c.Account_ID = a.Account_ID where a.Company_ID = %s and c.customer_declaration_date is null
            """
            
        elif body['mode'] == "5":
            query = """
            
            SELECT * FROM Customer c join Account a on c.Account_ID = a.Account_ID where a.Company_ID = %s
            
            """
            
        elif body['mode'] == "4":
            return JSONResponse(content=await getCount(body['wholesellerID'], body['compID']), status_code=200)
            
        values = (body['compID'],)
            
        cursor.execute(query, values)
        result = cursor.fetchall()
        
        columnnName = [desc[0] for desc in cursor.description]

        if result and len(list(result)) > 0:
            for row in list(result):
                rowDict = {}
                
                for i, col_name in enumerate(columnnName):
                    if str(row[i]).replace(" ", "") == "":
                        rowDict[col_name] = ""
                    else:
                        if col_name == 'Customer_PDPA_Date' or col_name == 'Customer_Declaration_Date' or col_name == 'Customer_Migration_Date':
                            try:
                                dateObject = datetime.strptime(str(row[i]), "%Y-%m-%d %H:%M:%S")
                                formattedDate = dateObject.strftime("%d/%m/%Y %H:%M:%S")
                                rowDict[col_name] = str(formattedDate)
                            except Exception as e:
                                rowDict[col_name] = str(row[i])
                        else:
                            rowDict[col_name] = str(row[i])

                resultDict.append(rowDict)
        
        await closeConn(cursor, conn_ng999)
        return JSONResponse(content=resultDict, status_code=200)
            
    except Exception as e:
        print(e, flush=True)
        await closeConn(cursor, conn_ng999)
        return JSONResponse(content={}, status_code=400)
    
    
@app.post("/ng999/company/insertCompany")
async def insertCompany(request:Request):
    try:
        body = await request.json()
        
        conn_ng999 = await getSqlCONN()
        cursor = conn_ng999.cursor()
        conn_ng999.begin()
        
        query = """
        insert into Company (Company_Name,Company_Date_Created) values (%s,%s);
        """
    
        values = (body['Name'],datetime.now())
        
        cursor.execute(query, values)
        
        if cursor.rowcount > 0:
            conn_ng999.commit()
            await closeConn(cursor, conn_ng999)
            return JSONResponse(content={}, status_code=200)
        
        await closeConn(cursor, conn_ng999)
        return JSONResponse(content={}, status_code=400)
    
    except Exception as e:
        print(e, flush=True)
        await closeConnRollback(cursor, conn_ng999)
        return JSONResponse(content={}, status_code=400)
    
    
@app.post("/ng999/company/deleteCompany")
async def deleteCompany(request:Request):
    try:
        body = await request.json()
        
        conn_ng999 = await getSqlCONN()
        cursor = conn_ng999.cursor()
        conn_ng999.begin()
        
        query = """
        
        delete from Company where Company_ID = %s;
        """
    
        values = (body['ID'],)
        
        cursor.execute(query, values)
        
        if cursor.rowcount > 0:
            conn_ng999.commit()
            await closeConn(cursor, conn_ng999)
            return JSONResponse(content={}, status_code=200)
        
        await closeConn(cursor, conn_ng999)
        return JSONResponse(content={}, status_code=400)
    
    except Exception as e:
        print(e, flush=True)
        await closeConnRollback(cursor, conn_ng999)
        return JSONResponse(content={}, status_code=400)
    

@app.post("/ng999/company/declare")
async def declareCompany(request:Request):
    try:
        body = await request.json()
        
        if body['bundle'] == '0':
            if await checkCustDBDeclare(body['CustID'], body['PhoneNo']):
                return JSONResponse(content={'Message': "Duplicated Phone Number"}, status_code=400)
        
        conn_ng999 = await getSqlCONN()
        cursor = conn_ng999.cursor()
        conn_ng999.begin()
        
        query = """
        
        update Customer set Customer_PDPA_Date = %s, Customer_Declaration_Date = %s, Customer_Name = %s, Customer_Additional_Info = %s, Customer_Address = %s, Customer_Phone_Number = %s where Customer_ID = %s;
        """
    
        values = (datetime.now(), datetime.now(), body['Name'], body['AdditionalInfo'], body['Address'], body['PhoneNo'], body['CustID'])
        
        cursor.execute(query, values)
        
        if cursor.rowcount > 0:
            conn_ng999.commit()
            await closeConn(cursor, conn_ng999)
            return JSONResponse(content={}, status_code=200)
        
        await closeConn(cursor, conn_ng999)
        return JSONResponse(content={}, status_code=400)
    
    except Exception as e:
        print(e, flush=True)
        await closeConnRollback(cursor, conn_ng999)
        return JSONResponse(content={'Message': str(e)}, status_code=400)
    
    
@app.get("/ng999/admin/dashboard")
async def adminDashboard():
    try:
        finalList = {}
        
        conn_ng999 = await getSqlCONN()
        cursor = conn_ng999.cursor()
        
        query = """
        select count(*) from Company
        """
        
        
        queryList = [
            
            """
            select count(*) from Company;
            """,
            """
            select count(*) from Account where isActive = True and Account_Role = '2';
            """,
            """
            select count(*) from Account where isActive = False and Account_Role = '2';
            """,
            
            """
            select count(*) from Customer;
            """
        ]
        
        
        for i, q in enumerate(queryList):
            cursor.execute(q)
            result = cursor.fetchall()
            
            if result is not None and len(list(result)) > 0:
                if i == 0:
                    finalList['wholeSaler'] = list(list(result)[0])[0]
                elif i == 1:
                    finalList['active'] = list(list(result)[0])[0]
                elif i == 2:
                    finalList['inactive'] = list(list(result)[0])[0]
                else:
                    finalList['totalCust'] = list(list(result)[0])[0]
                    
        await closeConn(cursor, conn_ng999)
                
        return JSONResponse(content=finalList, status_code=200)
        
    except Exception as e:
        print(str(e), flush=True)
        await closeConn(cursor, conn_ng999)
        return JSONResponse(content={'Message': str(str(e))}, status_code=400)
    

@app.post("/ng999/customer/bundleDeclare")
async def bundleDeclare(request:Request):
    try:
        body = await request.json()
        conn_ng999 = await getSqlCONN()

        conn_ng999.begin()
        cursor = conn_ng999.cursor()

        for cust in body['custID']:
            query = """
            
            update Customer set Customer_PDPA_Date = %s, Customer_Declaration_Date = %s where Customer_ID = %s
            
            """
            values = (datetime.now(), datetime.now(), cust)
            
            cursor.execute(query, values)
        
        if cursor.rowcount > 0:
            conn_ng999.commit()
        
        await closeConn(cursor, conn_ng999)
        
        return JSONResponse(content={}, status_code=200)
                
    except Exception as e:
        print(e, flush=True)
        await closeConnRollback(cursor, conn_ng999)
        return JSONResponse(content={}, status_code=400)
        
@app.post("/ng999/account/updateInfo")
async def updateAccInfo(request:Request):
    try:
        body = await request.json()
        conn_ng999 = await getSqlCONN()

        conn_ng999.begin()
        cursor = conn_ng999.cursor()
        
        if await checkEmail(body['email'], body['accID']) or await checkPhoneNumber(body['PhoneNo'], body['accID']):
            await closeConn(cursor, conn_ng999)
            return JSONResponse(content={}, status_code=400)
            
        query = """
        
        update Account set Account_Name = %s, Account_Phone_Number = %s, Account_Email = %s, isActive = %s, lastActive = %s where Account_ID = %s
        
        """
        values = (body['name'], body['PhoneNo'], body['email'], body['status'], datetime.now(), body['accID'])
        
        cursor.execute(query, values)
        
        if cursor.rowcount > 0:
            conn_ng999.commit()
        
        await closeConn(cursor, conn_ng999)
        
        return JSONResponse(content={}, status_code=200)
                
    except Exception as e:
        print(e, flush=True)
        await closeConnRollback(cursor, conn_ng999)
        return JSONResponse(content={}, status_code=400)
    
@app.post("/ng999/customer/getWholeSalerCust")
async def getWholeSalerFromBilling(request:Request):
    try:
        resultDict = []
        body = await request.json()
        
        conn_ng999 = await getMSSQLConn()
        cursor = conn_ng999.cursor()
        
        query = """
            SELECT
            a.AccountID as 'CustID', b.Name as 'Name', b.Address as 'Address', b.Address1 as 'Address1', b.Address2  as 'Address2', b.Address3  as 'Address3', e.callerid as 'CallerNo'
            FROM [dbo].[Account_MasterData] a
            LEFT JOIN [dbo].[Customer] b
                ON a.accountid = b.custid
            LEFT JOIN [NewIddGateway].[NewIddGateway].[dbo].[UserDetailExt] c
                ON CONVERT(VARCHAR, a.accountid) = c.accountid
            LEFT JOIN [NewIddGateway].[NewIddGateway].[dbo].[UserDetail] d
                ON CONVERT(VARCHAR, a.accountid) = d.accountid

            LEFT JOIN [NewIddGateway].[NewIddGateway].[dbo].[Authentication] e
                on convert(varchar, a.accountid) = e.accountid

            WHERE[WholeSaleID] = %s and e.CallerID NOT IN (SELECT
                CallerID
                FROM [NewIddGateway].[NewIddGateway].dbo.[Authentication] c
                INNER JOIN [NewIddGateway].[NewIddGateway].dbo.BB_Authentication d
                ON c.CallerID = d.bb_RT015 where c.callerID = convert(varchar, a.AccountID))
                
                """

        values = (body['wholeSalerID'],)
        cursor.execute(query, values)
        result = cursor.fetchall()
                
        columnnName = [desc[0] for desc in cursor.description]

        for row in list(result):
            rowDict = {}
            for i, col_name in enumerate(columnnName):
                if row[i] == None:
                    rowDict[col_name] = ""
                else:
                    rowDict[col_name] = str(row[i])
            
            resultDict.append(rowDict)
            
       
        await closeConn(cursor, conn_ng999)
        return JSONResponse(content=resultDict, status_code=200)
        
    except Exception as e:
        print(e, flush=True)
        await closeConn(cursor, conn_ng999)
        return JSONResponse(content=[], status_code=400)
        
        
    
async def getSqlCONN():
    return MySQLdb.connect('192.168.138.213', 'NG999', 'l]tb8/Eog2q[X5rC', 'NG999') 

async def getMSSQLConn():
    return pymssql.connect(server='192.168.138.120', user='GuestReadOnly', password='GuestReadOnly', database='Online_WS_CallBilling')


async def closeConnRollback(cursor=None, conn_ng999=None):
    try:
        conn_ng999.rollback()
        cursor.close()
        conn_ng999.close()
    except Exception as e:
        pass
    
async def closeConn(cursor=None, conn_ng999=None):
    try:
        cursor.close()
        conn_ng999.close()
    except Exception as e:
        pass
    
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8888)