import pymssql
import pyodbc

def getMSSQLConn():
    print(pyodbc.drivers())
    connection_string = 'DRIVER=ODBC Driver 17 for SQL Server;SERVER=192.168.138.120;DATABASE=Online_WS_CallBilling;UID=GuestReadOnly;PWD=GuestReadOnly;'
    # return pymssql.connect(server='192.168.138.120', user='GuestReadOnly', password='GuestReadOnly', database='Online_WS_CallBilling')
    return pyodbc.connect(connection_string)

con = getMSSQLConn()
cursor = con.cursor()


query = """

            SELECT
            a.AccountID, b.Address, b.Address1, b.Address2, b.Address3, b.Name, e.callerid
            FROM [dbo].[Account_MasterData] a
            LEFT JOIN [dbo].[Customer] b
                ON a.accountid = b.custid
            LEFT JOIN [NewIddGateway].[NewIddGateway].[dbo].[UserDetailExt] c
                ON CONVERT(VARCHAR, a.accountid) = c.accountid
            LEFT JOIN [NewIddGateway].[NewIddGateway].[dbo].[UserDetail] d
                ON CONVERT(VARCHAR, a.accountid) = d.accountid

            LEFT JOIN [NewIddGateway].[NewIddGateway].[dbo].[Authentication] e
                on convert(varchar, a.accountid) = e.accountid

            WHERE[WholeSaleID] = ? and e.CallerID NOT IN (SELECT
                CallerID
                FROM [NewIddGateway].[NewIddGateway].dbo.[Authentication] c
                INNER JOIN [NewIddGateway].[NewIddGateway].dbo.BB_Authentication d
                ON c.CallerID = d.bb_RT015 where c.callerID = convert(varchar, a.AccountID))
                
        """

values = ('8000014',)
cursor.execute(query, values)
result = cursor.fetchall()
columnnName = [desc[0] for desc in cursor.description]


resultDict = []

finalDict = []



for row in list(result):
    rowDict = {}
    for i, col_name in enumerate(columnnName):
        rowDict[col_name] = str(row[i])
    
    resultDict.append(rowDict)
                    

cursor.close()
con.close()

for i in resultDict:
    print(i)
    print('\n')    