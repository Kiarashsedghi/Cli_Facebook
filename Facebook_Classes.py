from getpass import getpass
import pymssql
import re


class FacebookCliRegexes:
    def __init__(self):
        self.login='^\s*login\s*$'
        self.signup="^\s*signup\s*$"
        self.exit="^\s*(exit|bye)\s*$"


class FacebookUserCredentials:
    def __init__(self,username,password):
        self.username=username
        self.password=password




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

        self.server_hd.execute("select * from users where username='{0}' and password='{1}'".format(username,password))
        if len(self.server_hd.fetchall())==0:
            return 0
        return 1



class FacebookCli:
    def __init__(self):
        self.dbhandler=None
        self.usercred_obj=None

        # pagename is for prompt:   pagename>
        self.pagename=''
        self.usercmd=None
        self.cmdrgx_obj=None


    def get_userpass(self):
        '''
        Prompting and asks users for their username and password
        :return:(username,password)
        '''
        username=input("Username: ")
        password=getpass("Password: ")
        return username,password

    def initialize(self):

        '''
        This function initializes the program by creating database handler object
        ,creating Cli cmd regex object
        :return: status of initialization
                [if] program fails while connecting to database it will exit with status of 5
                [else] returns 0 to the main program
        '''

        # Create Facebook database handler
        # TODO‌ reading from a file / more secure than below
        self.dbhandler = FacebookDB("192.168.200.6", "Facebook", "sa", "abracadabra")
        if self.dbhandler.connect() is None:
            self.printe("Cannot connect to database... ")
            exit(5)
        else:
            # Create cli command regex object
            self.cmdrgx_obj=FacebookCliRegexes()
            return 0

    def prompt(self):
        '''
        This function gives the cli prompt to the user
        '''

        print("\tWelcome to Facebook CLI")
        print("---Quick Help---")
        print("login ,for login to your account")
        print("signup , for create new account")
        print("----------------")

        while(True):
            self.usercmd=input("{0}> ".format(self.pagename))

            if re.match(self.cmdrgx_obj.login, self.usercmd) is not None:

                # Create user credentials handler for the program
                self.usercred_obj = FacebookUserCredentials(*self.get_userpass())

                # Authenticate user
                if self.dbhandler.authenticate_user(username=self.usercred_obj.username, password=self.usercred_obj.password):
                    print("Welcome {0}".format(self.usercred_obj.username))

                else:
                    self.printe("Authentication Failed")

            elif re.match(self.cmdrgx_obj.signup, self.usercmd) is not None:
                print("sign up issued")

            elif re.match(self.cmdrgx_obj.exit, self.usercmd) is not None:
                print("Bye! See you later")
                exit(0)

    def printe(self,message):
        #TODO‌ color
        print(message)