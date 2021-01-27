import pymssql
from datetime import datetime
class FacebookDB:

    def __init__(self,server_addr,db_name,username,password):
        self.server_hd=None
        self.server_properties = {
             'host' : server_addr,
             'database' : db_name,
             'user' : username,
             'password' : password
             }

    def connect(self):
        '''
        This function connects to database and returns an handler to work with the database
        :return: database handler
        '''
        self.server_hd=(pymssql.connect(**self.server_properties)).cursor()
        return self.server_hd


    def authenticate_user(self,username,password):
        '''
        This function authenticates user based on username and password user provided
        :param username:
        :param password:
        :return: returns 1 if authentication was successful else 0
        '''

        self.server_hd.execute("select * from users where email='{0}' and password='{1}'".format(username,password))
        if len(self.server_hd.fetchall())==0:
            return 0
        return 1

    def is_username_taken(self,username):
        '''
        This function checks whether username is already taken or not
        :param username:
        :return: returns 1 if username has been already taken else 0
        '''
        self.server_hd.execute("select * from users where email='{0}'".format(username))
        if len(self.server_hd.fetchall())==0:
            return 0
        return 1

    def create_user(self,**user_info):
        firstname=user_info['firstname']
        lastname=user_info['lastname']
        username=user_info['email']
        password=user_info['password']
        gender=user_info['gender']
        phonenumber=user_info['phonenumber']
        birthdate=user_info['birthdate']

        sql_string="'{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}'".format(firstname,lastname,birthdate,gender,phonenumber,password,
                                    username,'1111111','NULL','NULL','NULL','NULL')



        self.server_hd.execute("insert into users values({0})".format(sql_string))



    def update_user_by_username(self,username,**user_info):
        bio=user_info['bio'] if len(user_info['bio'])!=0 else 'NULL'
        currentcityname=user_info['currentcityname'] if len(user_info['currentcityname'])!=0 else 'NULL'
        hometownname=user_info['hometownname'] if len(user_info['hometownname'])!=0 else 'NULL'
        relationshipstatus=user_info['relationshipstatus'] if len(user_info['relationshipstatus'])!=0 else 'NULL'

        sql_string="set bio='{0}',currentcityname='{1}',hometownname='{2}',relationshipstatus='{3}'"
        self.server_hd.execute("update users {0} where email='{1}'".format(sql_string,username))




