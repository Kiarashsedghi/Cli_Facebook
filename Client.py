from Server import *
from lib import *
import re
from datetime import datetime

from getpass import getpass


class FacebookCli:
    def __init__(self):
        self.dbhandler = None
        self.usercred_obj = None

        # pagename is for prompt:   pagename>
        self.usercmd = None
        self.cmdrgx_obj = None

    def get_userpass(self):
        '''
        Prompting and asks users for their username and password
        :return:(username,password)
        '''
        username = input("Username: ")
        password = getpass("Password: ")
        return username, password

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
        self.dbhandler = FacebookDB(
            "127.0.0.1", "Facebook", "SA", "@1378Alisajad")
        if self.dbhandler.connect() is None:
            self.printe("Cannot connect to database... ")
            exit(5)
        else:
            # Create cli command regex object
            self.cmdrgx_obj = FacebookCliRegexes()
            return 0

    def login(self):
        # Create user credentials handler for the program

        username, password = self.get_userpass()

        # Authenticate user
        if self.dbhandler.authenticate_user(username=username, password=password):
            return FacebookUserCredentials(username, password)

        return None

    def signup(self):
        '''
        This function register new user
        :return:
        '''

        # name = "kiarash"
        # lastname = "s"
        # password = "123"
        # gender = "male"
        # dateofbirth="11-11-1111"
        # phonenumber="123213123"
        # username="kia"
        name = str()
        lastname = str()
        password = str()
        gender = str()
        dateofbirth = str()
        phonenumber = str()
        username = str()
        while (len(name) == 0):
            name = (input("name: ")).strip()
        while (len(lastname) == 0):
            lastname = (input("lastname: ")).strip()

        while (1):
            username = (input("username: ")).strip()
            if self.dbhandler.is_username_taken(username):
                self.printe(
                    "username {0} has been already taken".format(username))
                continue
            elif len(username) == 0:
                continue
            elif not (re.match(self.cmdrgx_obj.email, username)):
                self.printe("Not a valid email address entered")
                continue
            break

        while (len(password) == 0):
            password = (getpass("password: ")).strip()
        while (len(gender) == 0) and (not re.match(self.cmdrgx_obj.gender, gender)):
            gender = (input("gender[male/female]: ")).strip()
        while (len(dateofbirth) == 0) and (not re.match(self.cmdrgx_obj.date_of_birth, dateofbirth)):
            dateofbirth = (input("date of birth[DD-MM-YYYY]: ")).strip()

        while (len(phonenumber) == 0):
            phonenumber = input("phone number: ")

        self.dbhandler.create_user(firstname=name, lastname=lastname, email=username,
                                   password=password, gender=gender, birthdate=dateofbirth, phonenumber=phonenumber)

        while(1):
            self.usercmd = input("Continue upgrading account?[yes/no]: ")
            if(re.match(self.cmdrgx_obj.yes_ans, self.usercmd)):

                bio = input("bio: ")
                current_city = input("current_city: ")
                hometown = input("hometown: ")
                relationship_status = input("relationship[married/single]: ")
                self.dbhandler.update_user_by_username(
                    username, bio=bio, currentcityname=current_city, hometownname=hometown, relationshipstatus=relationship_status)
                break
            elif(re.match(self.cmdrgx_obj.no_ans, self.usercmd)):
                break

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
            self.usercmd = input("> ")

            if re.match(self.cmdrgx_obj.login, self.usercmd) is not None:
                login_object = self.login()
                if login_object:
                    print("Welcome {0}".format(login_object.username))
                else:
                    print("username or password is incorrect :(")

            # Create new user
            elif re.match(self.cmdrgx_obj.signup, self.usercmd) is not None:
                self.signup()

            elif re.match(self.cmdrgx_obj.exit, self.usercmd) is not None:
                print("Bye! See you later")
                exit(0)

    def printe(self, message):
        # TODO‌ color
        print(message)


client_obj = FacebookCli()
client_obj.initialize()
client_obj.prompt()
