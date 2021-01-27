import pymssql

server_properties = {
             'host' : '192.168.200.6',
             'database' : 'Facebook',
             'user' : 'sa',
             'password' : 'abracadabra'
             }
q=pymssql.connect(**server_properties)
q=q.cursor()

q.execute("select * from users where username='{0}' and password='{1}'".format('ma77','ma1999'))
print(q.fetchall())
