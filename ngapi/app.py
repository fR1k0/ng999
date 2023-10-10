from fastapi import FastAPI, APIRouter, Depends, HTTPException, Request
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



app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
data = []
conn_ng999 = MySQLdb.connect('192.168.138.213', 'NG999', 'l]tb8/Eog2q[X5rC', 'NG999') 


class Company(BaseModel):
   Company_ID: int | None = None
   Company_Name: str
   Company_Date_Created: date

# Route to create an item
# @app.post("/ng999/company/add",response_model=Company)
# def add_ng999_company_data(company: Company):
# 	#return company.Company_ID
#     try:
#         cursor = conn_ng999.cursor()
#         conn_ng999.begin()
        
#         query = "insert into Company (Company_Name,Company_Date_Created) values (%s,%s)"
        
#         cursor.execute(query, (company.Company_Name,company.Company_Date_Created,))
#         conn_ng999.commit()
        
#         company.Company_ID = cursor.lastrowid
#         if cursor: cursor.close()
        
#         return company
    
#     except Exception as e:
#         print(e)
#         conn_ng999.rollback()
#         if cursor: cursor.close()
        
#         return JSONResponse(content={}, status_code=404)
    
def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))
    
    return password

async def checkEmail(email):
    cursor = conn_ng999.cursor()
    query = """

    select * from Account where Account_Email = %s
    
    """
    values = (email, )
    
    cursor.execute(query, values)
    
    result = cursor.fetchone()
    
    if result is not None and len(list(result)) > 0:
        if cursor: cursor.close()
        return True
    
    cursor.close()
    return False
    
@app.post("/ng999/account/add")
async def add_ng999_company_data(request: Request):
    password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    try:
        
        body = await request.json()
        
        if await checkEmail(body['email']):
            return JSONResponse(content={}, status_code=404)
        
        cursor = conn_ng999.cursor()
        conn_ng999.begin()
        
        # Will use it later 
        # password = generate_password()
        password = "P@ssw0rd2288"
        
        hashPassword = password_context.hash(password)
    
        query = """
        
        insert into Account (Account_Password, Account_name, Account_Role, Account_date_Created, Company_ID, Account_Email) 
        values (%s, %s, %s, %s, %s, %s)
        
        """
        
        values = (hashPassword, body['name'], body['role'], datetime.now(), body['wholesellerID'], body['email'] )
        cursor.execute(query, values)
        
        if cursor.rowcount > 0:
            conn_ng999.commit()
            if cursor: cursor.close()
            return JSONResponse(content={}, status_code=200)
    
    except Exception as e:
        print(e, flush=True)
        conn_ng999.rollback()
        if cursor: cursor.close()
        
        return JSONResponse(content={}, status_code=404)
    
@app.post("/ng999/logon")
async def ng999_logon(request:Request):
    try:
        password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        body = await request.json()
        cursor = conn_ng999.cursor()
        
        query = "select account_password, account_role, account_email, account_id, account_name from Account where account_email = %s"
        
        values = (body['username'],)
        cursor.execute(query, values)
        result = cursor.fetchone()
                        
        if result:
            if list(result)[0] is not None:                
                if password_context.verify(body['password'], list(result)[0]):
                    if cursor: cursor.close()
                    return JSONResponse(content={'user_id': list(result)[3], 'username': list(result)[2], 'role': list(result)[1], 'accountName': list(result)[4]}, status_code=200)
                
        return JSONResponse(content={'Message': "Incorrect Password"}, status_code=404)
                
    except Exception as e:
        print(e)
        if cursor: cursor.close()
        return JSONResponse(content={}, status_code=404)


# Route to read an item   
@app.get("/ng999/company/get/{id}")
def get_ng999_company_data(Company_ID: int):
    try:
        cursor = conn_ng999.cursor()
        
        query = "SELECT Company_ID , Company_Name, Company_Date_Created FROM Company WHERE Company_ID=%s"
        cursor.execute(query, (Company_ID,))
        
        item = cursor.fetchone()
        if cursor: cursor.close()
        
        
        if item is None:
            raise HTTPException(status_code=404, detail="Data not found")
        
        return {"Company_ID": item[0], "Company_Name": item[1], "Company_Date_Created": item[2]}
    
    except Exception as e:
        print(e)
        if cursor: cursor.close()
        
        return JSONResponse(content={}, status_code=404)


# Route to update an item
@app.put("/ng999/company/update/{Company_ID}", response_model=Company)
def update_ng999_company_data(Company_ID: int, company: Company):
    try:
        cursor = conn_ng999.cursor()
        conn_ng999.begin()
        
        query = "UPDATE Company SET Company_Name=%s, Company_Date_Created=%s WHERE Company_ID=%s"
        
        cursor.execute(query, (company.Company_Name, company.Company_Date_Created, Company_ID))
        conn_ng999.commit()
        
        company.Company_ID = Company_ID
        
        if cursor: cursor.close()
    
        return company

    except Exception as e:
        print(e)
        
        conn_ng999.rollback()
        if cursor: cursor.close()
        
        return JSONResponse(content={}, status_code=404)

# Route to delete an item
@app.delete("/ng999/company/delete/{id}")
def delete_ng999_company_data(Company_ID: int):
    try:
        cursor = conn_ng999.cursor()
        conn_ng999.begin()
        
        query = "DELETE FROM Company WHERE Company_ID=%s"
        cursor.execute(query, (Company_ID,))
        
        conn_ng999.commit()
        if cursor: cursor.close()
        
        return {"Company_ID": Company_ID}
    
    except Exception as e:
        print(e)
        conn_ng999.rollback()
        if cursor: cursor.close()
        
        return JSONResponse(content={}, status_code=404)
   

@app.get("/ng999/company/list")
def get_ng999_company_datas():
    try:
        cursor = conn_ng999.cursor()
        
        query = "SELECT * FROM Company where Company_ID"
        cursor.execute(query)
        item = cursor.fetchall()
        
        columnnName = [desc[0] for desc in cursor.description]
        resultDict = []
        
        if item is None:
            raise HTTPException(status_code=404, detail="Data not found")
        
        for row in list(item):
            rowDict = {}
            for i, col_name in enumerate(columnnName):
                rowDict[col_name] = str(row[i])
            
            resultDict.append(rowDict)
        
        return resultDict
    
    except Exception as e:
        print(e)
        if cursor: cursor.close()
        
        return JSONResponse(content={}, status_code=404)
    
@app.get("/ng999/account/list")
def getAccountList():
    try:
        cursor = conn_ng999.cursor()
        
        query = "SELECT * FROM Account a join Company c on a.company_id = c.company_id where a.Account_Role = '2'"
        cursor.execute(query)
        item = cursor.fetchall()
        
        columnnName = [desc[0] for desc in cursor.description]
        resultDict = []
        
        if item is None:
            raise HTTPException(status_code=404, detail="Data not found")
        
        for row in list(item):
            rowDict = {}
            for i, col_name in enumerate(columnnName):
                rowDict[col_name] = row[i]
            
            resultDict.append(rowDict)
        
        return resultDict
    
    except Exception as e:
        print(e)
        if cursor: cursor.close()
        
        return JSONResponse(content={}, status_code=404)
    
async def checkCustDB(accountID, phoneNumber):
    try:
        cursor = conn_ng999.cursor()
        query = """
    
        select * from Customer where account_id = %s and Customer_Phone_Number = %s
        """
        
        values = (accountID, phoneNumber)
        cursor.execute(query, values)
        
        result = cursor.fetchone()
        
        if result and len(list(result)) > 0:
            if cursor: cursor.close()
            return True 
        
        if cursor: cursor.close()
        return False
    
    except Exception as e:
        print(e)
        if cursor: cursor.close()
        return False
    
async def checkCustDBDeclare(custID, phoneNumber):
    try:
        cursor = conn_ng999.cursor()
        query = """
    
        select * from Customer where Customer_ID != %s and Customer_Phone_Number = %s
        """
        
        values = (custID, phoneNumber)
        cursor.execute(query, values)
        
        result = cursor.fetchone()
        
        if result and len(list(result)) > 0:
            if cursor: cursor.close()
            return True 
        
        if cursor: cursor.close()
        return False
    
    except Exception as e:
        print(e)
        if cursor: cursor.close()
        return False
    
    
@app.post("/ng999/customer/add")
async def get_ng999_company_datas(request:Request):
    try:
        body = await request.json()
    
        cursor = conn_ng999.cursor()
        conn_ng999.begin()
        
        for i in body['data']:
            # No duplicated phone number can be inserted to the db
            if i['CarllerNo'].replace(" ", "") == "":
                continue
            
            if await checkCustDB(body['wholesellerID'], i['CarllerNo']):
                continue
            
            print(i['CarllerNo'], flush=True)
            query = """
            
            Insert into Customer (Customer_Name, Customer_Migration_Date,
            Customer_Address, Customer_Phone_Number, Customer_Additional_Info, Account_ID, CustBillingID) 
            values (%s, %s, %s, %s, %s, %s, %s);
    
            """
            values = (i['Name'], datetime.now(), i['Address'] + " " + i['Address1'] + " " + i['Address2'] + " " + i['Address3'], i['CarllerNo'], i['WholeSaleID'], body['wholesellerID'], i['CustID'])

            cursor.execute(query, values)
        
        conn_ng999.commit()
        if cursor: cursor.close()
        return JSONResponse(content={}, status_code=200)
        
        
    except Exception as e:
        print(e)
        conn_ng999.rollback()
        if cursor: cursor.close()
        return JSONResponse(content={}, status_code=404)
    
async def getCount(wholesellerID):
    try:
        body = {"active": 0, "totalUser": 0, "withMigrate": 0, "withoutMigrate": 0}
        
        cursor = conn_ng999.cursor()
        
        queryList = ["""
        select count(*) from Customer where Account_ID = %s
        """,
        """
        select count(*) from Customer where Account_ID = %s and customer_declaration_date is not null
        
        """,
        """
        select count(*) from Customer where Account_ID = %s and customer_declaration_date is null
        """]
        
        for index, q in enumerate(queryList):
            
            values = (wholesellerID, )
            cursor.execute(q, values)
            
            result = cursor.fetchone()
            
            if result and len(list(result)) > 0:
                
                if index == 0:
                    body['totalUser'] = list(result)[0]
                elif index == 1:
                    body['withMigrate'] = list(result)[0]
                else:
                    body['withoutMigrate'] = list(result)[0]
        
        if cursor: cursor.close()
        return body
    
    except Exception as e:
        print(e)
        return {}
                

@app.post("/ng999/customer/getList")
async def get_ng999_company_datas(request:Request):
    try:
        body = await request.json()
        
        cursor = conn_ng999.cursor()
        resultDict = []
        
        query = """
        select * from Customer where Account_ID = %s and date(customer_migration_date) = curdate()
        """
        
        if body['mode'] == "1":
            query = """
            select * from Customer where Account_ID = %s and customer_declaration_date is not null
            """
        elif body['mode'] == "2":
            query = """
            
            select * from Customer where Account_ID = %s and customer_declaration_date is null
            """
            
        elif body['mode'] == "4":
            return JSONResponse(content=await getCount(body['wholesellerID']), status_code=200)
            
        values = (body['wholesellerID'],)
            
        cursor.execute(query, values)
        result = cursor.fetchall()
        
        columnnName = [desc[0] for desc in cursor.description]

        if result and len(list(result)) > 0:
            for row in list(result):
                rowDict = {}
                
                for i, col_name in enumerate(columnnName):
                    rowDict[col_name] = str(row[i])

                resultDict.append(rowDict)
        
        if cursor: cursor.close()
        return JSONResponse(content=resultDict, status_code=200)
            
    except Exception as e:
        print(e)
        if cursor: cursor.close()
        return JSONResponse(content={}, status_code=404)
    
    
@app.post("/ng999/company/insertCompany")
async def insertCompany(request:Request):
    try:
        body = await request.json()
        
        conn_ng999.begin()
        cursor = conn_ng999.cursor()
        
        query = """
        insert into Company (Company_Name,Company_Date_Created) values (%s,%s);
        """
    
        values = (body['Name'],datetime.now())
        
        cursor.execute(query, values)
        
        if cursor.rowcount > 0:
            conn_ng999.commit()
            return JSONResponse(content={}, status_code=200)
    
    except Exception as e:
        conn_ng999.rollback()
        print(e, flush=True)
        return JSONResponse(content={}, status_code=404)
    
    
@app.post("/ng999/company/deleteCompany")
async def deleteCompany(request:Request):
    try:
        body = await request.json()
        
        conn_ng999.begin()
        cursor = conn_ng999.cursor()
        
        query = """
        
        delete from Company where Company_ID = %s;
        """
    
        values = (body['ID'],)
        
        cursor.execute(query, values)
        
        if cursor.rowcount > 0:
            conn_ng999.commit()
            
            if cursor:cursor.close()
            return JSONResponse(content={}, status_code=200)
    
    except Exception as e:
        conn_ng999.rollback()
        if cursor:cursor.close()
        print(e, flush=True)
        return JSONResponse(content={}, status_code=404)
    

@app.post("/ng999/company/declare")
async def declareCompany(request:Request):
    try:
        body = await request.json()
        
        if body['bundle'] == '0':
            if await checkCustDBDeclare(body['CustID'], body['PhoneNo']):
                return JSONResponse(content={'Message': "Duplicated Phone Number"}, status_code=404)
        
        conn_ng999.begin()
        cursor = conn_ng999.cursor()
        
        query = """
        
        update Customer set Customer_Declaration_Date = %s, Customer_Name = %s, Customer_Additional_Info = %s, Customer_Address = %s, Customer_Phone_Number = %s where Customer_ID = %s;
        """
    
        values = (datetime.now(), body['Name'], body['AdditionalInfo'], body['Address'], body['PhoneNo'], body['CustID'])
        
        cursor.execute(query, values)
        
        if cursor.rowcount > 0:
            conn_ng999.commit()
            if cursor:cursor.close()
            return JSONResponse(content={}, status_code=200)
    
    except Exception as e:
        conn_ng999.rollback()
        print(e, flush=True)
        if cursor:cursor.close()
        return JSONResponse(content={'Message': str(e)}, status_code=404)
    
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8888)
    

        
        