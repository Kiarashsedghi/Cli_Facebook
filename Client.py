from Server import *
from lib import *
import re
from time import sleep
from datetime import datetime

from getpass import getpass


class FacebookCli:
    def __init__(self):
        self.dbhandler = None
        self.usercred_obj = None

        # pagename is for prompt:   pagename>
        self.usercmd = None
        self.cmdrgx_obj = None

        self.pagectx = int()
        self.homepagectx = int()
        self.user_ans = str()

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

                bio = input("bio: ").strip()
                current_city = input("current_city: ").strip()
                hometown = input("hometown: ").strip()
                relationship_status = input(
                    "relationship[married/single]: ").strip()

                self.dbhandler.update_user_by_username(
                    username, bio=bio, currentcityname=current_city, hometownname=hometown, relationshipstatus=relationship_status)
                break
            elif(re.match(self.cmdrgx_obj.no_ans, self.usercmd)):
                break

        print("Creating page for you ...")
        sleep(2)
        self.dbhandler.create_new_page(username)
        self.usercred_obj = FacebookUserCredentials(username, password)
        print("Your page is ready")

    def show_homepage(self):
        userid, = self.dbhandler.get_user_info(
            "userid", username=self.usercred_obj.username)
        page_info = (self.dbhandler.get_page_info(
            "pagename", "pageid", userid=userid))
        pagename, self.homepagectx = page_info[0]
        self.pagectx = self.homepagectx

        while (True):
            self.usercmd = input("{0}> ".format(pagename))

            if re.match(self.cmdrgx_obj.exit, self.usercmd) is not None:
                print("exit from account!")
                return

            elif (re.match(self.cmdrgx_obj.post, self.usercmd) is not None) and self.pagectx == self.homepagectx:
                post_text = str()
                print('Enter Your Post Content:')
                temp = str()
                while len(temp) == 0 or temp != ".":
                    temp = (input()).strip()
                    post_text += temp+"\n"
                print("creating post...")
                sleep(1)
                if(self.dbhandler.create_new_post(
                        userid, post_text.strip()[:-1], self.pagectx, "Page")):
                    print("✅ post sent.")
                else:
                    print('❌ Post creation failed ')

            elif re.match(self.cmdrgx_obj.showpage, self.usercmd) is not None:
                page_contents = self.dbhandler.get_page_info(
                    "*", pageid=self.pagectx)
                page_posts = self.dbhandler.get_posts_by_page_id(
                    "*", destination=self.pagectx)
                print(page_contents, page_posts)

            elif re.match(self.cmdrgx_obj.like, self.usercmd) is not None:
                page_posts = self.dbhandler.get_posts_by_page_id(
                    '*', destination=self.pagectx)
                if len(page_posts):
                    for i in range(len(page_posts)):
                        print('{0}) -----------{1}-----------'.format(i +
                                                                      1, page_posts[i][3]))
                        post_like_count = (self.dbhandler.get_post_likes(
                            "count(*)", postid=page_posts[i][0]))[0][0]
                        print("👍 liked by {0} users\n".format(post_like_count))
                        print(page_posts[i][2]+'\n')
                        # Todo : likes count
                    while True:
                        self.user_ans = re.sub(
                            "\s*", "", input("👍 Which Post Do You Like? "))
                        if self.user_ans.isdigit() and (int(self.user_ans) in range(1, len(page_posts)+1)):
                            postid = page_posts[int(
                                self.user_ans)-1][0]
                            if self.dbhandler.like_post(postid, userid):
                                print("✅ Post Liked")
                            else:
                                print('❌ Post like failed ')
                            break
                else:
                    self.printe('No Post Exists.')

            elif re.match(self.cmdrgx_obj.dislike, self.usercmd) is not None:
                page_posts = self.dbhandler.get_posts_by_page_id(
                    '*', destination=self.pagectx)
                if len(page_posts):
                    for i in range(len(page_posts)):
                        print('{0}) -----------{1}-----------'.format(i +
                                                                      1, page_posts[i][3]))
                        post_like_count = (self.dbhandler.get_post_likes(
                            "count(*)", postid=page_posts[i][0]))[0][0]
                        print("👍 liked by {0} users\n".format(post_like_count))
                        print(page_posts[i][2]+'\n')
                        # Todo : likes count
                    while True:
                        self.user_ans = re.sub(
                            "\s*", "", input("👎 Which Post Do You dislike? "))
                        if self.user_ans.isdigit() and (int(self.user_ans) in range(1, len(page_posts)+1)):
                            postid = page_posts[int(
                                self.user_ans)-1][0]
                            if self.dbhandler.dislike_post(postid, userid):
                                print("✅ Post disliked")
                            else:
                                print('❌ Post dislike failed ')
                            break
                else:
                    self.printe('No Post Exists.')

            elif re.match(self.cmdrgx_obj.comment, self.usercmd) is not None:
                page_posts = self.dbhandler.get_posts_by_page_id(
                    '*', destination=self.pagectx)
                if len(page_posts):
                    for i in range(len(page_posts)):
                        print('{0}) -----------{1}-----------'.format(i +
                                                                      1, page_posts[i][3]))
                        post_comment_count = (self.dbhandler.get_post_comments(
                            "count(*)", postid=page_posts[i][0]))[0][0]
                        print("📃 {0} comments.\n".format(
                            post_comment_count))
                        print(page_posts[i][2]+'\n')
                        ##Todo : comments
                    while True:
                        self.user_ans = re.sub(
                            "\s*", "", input("📃 Which Post Do You Want To Comment? "))

                        if self.user_ans.isdigit() and (int(self.user_ans) in range(1, len(page_posts)+1)):
                            postid = page_posts[int(
                                self.user_ans)-1][0]
                            comments = self.dbhandler.get_post_comments(
                                'text', 'datetime', postid=postid)
                            if len(comments):
                                for i in range(len(comments)):
                                    print(
                                        '{0}) -----------{1}-----------'.format(i+1, comments[i][1]))
                                    print(comments[i][0]+'\n')
                            else:
                                print('No Comment')
                            comment_text = str()
                            temp = str()
                            print('Enter Your Comment:')
                            while len(temp) == 0 or temp != ".":
                                temp = (input()).strip()
                                comment_text += temp+"\n"
                            print('Creating Comment ...')
                            sleep(1)
                            if self.dbhandler.comment_post(postid, userid, comment_text):
                                print("✅ Comment Added ")
                            else:
                                print('❌ Add Comment Failed ')
                            break
                else:
                    self.printe('No Post Exists.')

            elif re.match(self.cmdrgx_obj.visitpage, self.usercmd) is not None:
                pagename = (self.usercmd).split()[1]
                query_result = self.dbhandler.get_page_info(
                    "pageid", pagename=pagename)
                if len(query_result) == 0:
                    print("Page {0} does not exist anymore".format(pagename))
                elif len(query_result) == 1:
                    self.pagectx = query_result[0][0]
                else:
                    print("which page do you want to visit?")
                    for i in range(len(query_result)):
                        print("{0}-{1} {2}".format(i+1,
                                                   pagename, query_result[i][0]))

                    while True:
                        self.user_ans = re.sub("\s*", "", input("?? "))
                        if self.user_ans.isdigit() and (int(self.user_ans) in range(1, len(query_result)+1)):
                            self.pagectx = query_result[int(
                                self.user_ans)-1][0]
                            break

            elif re.match(self.cmdrgx_obj.loadhomepage, self.usercmd) is not None:
                self.pagectx = self.homepagectx

            elif re.match(self.cmdrgx_obj.create_group, self.usercmd) is not None:
                grp_name = str()
                grp_description = str()

                while(len(grp_name) == 0):
                    grp_name = input('👨‍👩‍👦‍👦 Enter Your Group Name: ').strip()

                grp_description = input(
                    '🗒 Enter Your Group Description: ').strip()
                print('Creating Your Group For The First Time ...')
                sleep(1)
                if (self.dbhandler.create_new_group(userid, grp_name, grp_description)):
                    print('✅ Your Group Created Successfully')
                else:
                    print('❌ Group Creation Failed')

            elif re.match(self.cmdrgx_obj.show_group, self.usercmd) is not None:
                groups = self.dbhandler.get_groups_of_user(userid)
                if len(groups):
                    for i in range(len(groups)):
                        print('{0}.\t{1}\t{2}\n'.format(
                            i + 1, groups[i][0], '😎' if groups[i][1] == userid else ''))
                else:
                    print('No Groups Yet')
            elif re.match(self.cmdrgx_obj.add_member, self.usercmd) is not None:
                groups = self.dbhandler.get_groups_of_user(userid)
                if len(groups):
                    for i in range(len(groups)):
                        print('{0}.\t{1}\t{2}\n'.format(
                            i + 1, groups[i][0], '😎' if groups[i][1] == userid else ''))
                    while True:
                        self.user_ans = re.sub(
                            "\s*", "", input("📃 Which Group Do You Want To Add Member To? "))
                        if self.user_ans.isdigit() and (int(self.user_ans) in range(1, len(groups)+1)):
                            username = str()
                            while(len(username) == 0):
                                username = input('🥸 Enter Username: ').strip()
                            username_id = self.dbhandler.get_user_info(
                                'userid', username=username)[0]
                            print('Adding User To Group ...')
                            sleep(1)
                            if (self.dbhandler.add_member_to_group(groups[int(self.user_ans)-1][2], username_id)):
                                print('✅ User Added To Group Successfully')
                            else:
                                print('❌ User Addition Failed')
                            break

                else:
                    print('No Groups Yet')

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
                self.usercred_obj = self.login()
                if self.usercred_obj:
                    print("Welcome {0}".format(self.usercred_obj.username))
                    self.show_homepage()
                else:
                    print("username or password is incorrect :(")

            # Create new user
            elif re.match(self.cmdrgx_obj.signup, self.usercmd) is not None:
                self.signup()
                self.show_homepage()

            elif re.match(self.cmdrgx_obj.exit, self.usercmd) is not None:
                print("Bye! See you later")
                exit(0)

    def printe(self, message):
        # TODO‌ color
        print(message)


client_obj = FacebookCli()
client_obj.initialize()
client_obj.prompt()
