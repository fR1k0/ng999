import pymssql

def getMSSQLConn():
    return pymssql.connect(server='192.168.138.120', user='GuestReadOnly', password='GuestReadOnly', database='Online_WS_CallBilling')


print(getMSSQLConn)

cursor = getMSSQLConn().cursor()


query = """
 SELECT a.*
       ,b.*
       ,d.iSubType
       ,d.iRateType
       ,LEFT(d.iLang, LEN(d.iLang) - 1) AS LCRType
       ,d.iGateType
       ,d.PBXNo
       ,c.SIPSubType
       ,c.SIPLCRType
       ,c.IDDUsageAlert
       ,c.IDDUsageBar
       ,c.Note
       ,CASE a.[status]
          WHEN 1 THEN 'Active'
          WHEN 0 THEN 'Suspended'
          WHEN 2 THEN 'Locked'
        END AS status2
      FROM [dbo].[Account_MasterData] a
      LEFT JOIN [dbo].[Customer] b
        ON a.accountid = b.custid
      LEFT JOIN [NewIddGateway].[NewIddGateway].[dbo].[UserDetailExt] c
        ON CONVERT(VARCHAR, a.accountid) = c.accountid
      LEFT JOIN [NewIddGateway].[NewIddGateway].[dbo].[UserDetail] d
        ON CONVERT(VARCHAR, a.accountid) = d.accountid
"""

cursor.execute(query)


result = cursor.fetchall()


for row in list(result):
    print(row)