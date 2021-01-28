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
            "192.168.200.6", "Facebook", "SA", "abracadabra")
        if self.dbhandler.connect() is None:
            print("Cannot connect to database... ")
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
                print(
                    "username {0} has been already taken".format(username))
                continue
            elif len(username) == 0:
                continue
            elif not (re.match(self.cmdrgx_obj.email, username)):
                print("Not a valid email address entered")
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

    def print_group_posts(self, index ,post,liked_count,comment_count):

        print('-------------------------')
        print("{0}. By {1} On {2}".format(index + 1, post[0], post[2]))
        print("liked by {0} users".format(liked_count))
        print("{0} comments".format(comment_count))
        print("Content\n")
        print(post[1])



    def show_groupctx(self,groupid,grp_name,userid):


        while True:
            self.usercmd = input("G({0})> ".format(grp_name))

            if re.match(self.cmdrgx_obj.exit, self.usercmd) is not None:
                print("exit from group!")
                break

            elif re.match(self.cmdrgx_obj.show_members, self.usercmd) is not None:
                members=self.dbhandler.get_members_of_group(groupid)
                if len(members)==0:
                    print("No Member Exist In This Group")
                else:
                    #TODO show who is admin
                    for i in range(len(members)):
                        print("{0}. {1}".format(i+1,members[i][0]))

            #TODO‌ remove member

            elif re.match(self.cmdrgx_obj.post, self.usercmd) is not None:
                post_text=str()
                print('Enter Your Post Content:')
                temp = str()
                while len(temp) == 0 or temp!=".":
                    temp = (input()).strip()

                    post_text += temp + "\n"

                print("creating post...")
                sleep(1)
                if (self.dbhandler.create_new_post(
                        userid, post_text.strip()[:-1], groupid)):
                    print("✅ post sent.")
                else:
                    print('❌ Post creation failed ')

            elif re.match(self.cmdrgx_obj.show_group_posts, self.usercmd) is not None:
                posts=self.dbhandler.get_posts_of_group(groupid)
                if len(posts)==0:
                    print("No Has Posted Anything Yet")

                else:
                    for i in range(len(posts)):
                        post_like_count = (self.dbhandler.get_post_likes("count(*)", postid=posts[i][3]))[0][0]
                        post_comment_count = (self.dbhandler.get_post_comments("count(*)", postid=posts[i][3]))[0][0]
                        self.print_group_posts(i,posts[i],post_like_count,post_comment_count)

            elif re.match(self.cmdrgx_obj.like, self.usercmd) is not None:
                posts = self.dbhandler.get_posts_of_group(groupid)

                if len(posts):
                    for i in range(len(posts)):
                        post_like_count = (self.dbhandler.get_post_likes("count(*)", postid=posts[i][3]))[0][0]
                        post_comment_count = (self.dbhandler.get_post_comments("count(*)", postid=posts[i][3]))[0][0]
                        self.print_group_posts(i, posts[i], post_like_count, post_comment_count)

                    while True:
                            self.user_ans = re.sub(
                                "\s*", "", input("👍 Which Post Do You Like? "))
                            if self.user_ans.isdigit() and (int(self.user_ans) in range(1, len(posts)+1)):
                                postid = posts[int(self.user_ans)-1][3]
                                if self.dbhandler.like_post(postid, userid):
                                    print("✅ Post Liked")
                                else:
                                    print('❌ Post like failed ')
                                break
                else:
                    print('No Post Exists.')

            elif re.match(self.cmdrgx_obj.comment, self.usercmd) is not None:
                posts = self.dbhandler.get_posts_of_group(groupid)

                if len(posts):
                    for i in range(len(posts)):
                        post_like_count = (self.dbhandler.get_post_likes("count(*)", postid=posts[i][3]))[0][0]
                        post_comment_count = (self.dbhandler.get_post_comments("count(*)", postid=posts[i][3]))[0][0]
                        self.print_group_posts(i, posts[i], post_like_count, post_comment_count)

                    while True:
                        self.user_ans = re.sub("\s*", "", input("📃 Which Post Do You Want To Comment? "))

                        if self.user_ans.isdigit() and (int(self.user_ans) in range(1, len(posts) + 1)):
                            postid = posts[int(self.user_ans) - 1][3]


                            comment_text = str()
                            temp = str()
                            print('Enter Your Comment:')
                            while len(temp) == 0 or temp != ".":
                                temp = (input()).strip()
                                comment_text += temp + "\n"

                            comment_text=comment_text.strip()[:-1]

                            print('Creating Comment ...')
                            sleep(1)
                            if self.dbhandler.comment_post(postid, userid, comment_text):
                                print("✅ Comment Added ")
                            else:
                                print('❌ Add Comment Failed ')
                            break


                else:
                    print('No Post Exists.')


            elif re.match(self.cmdrgx_obj.show_comments_of_post, self.usercmd) is not None:
                posts = self.dbhandler.get_posts_of_group(groupid)

                if len(posts):
                    self.user_ans = re.sub("\s*", "", input("📃 Which Post Do You Want To See Comments? "))

                    if self.user_ans.isdigit() and (int(self.user_ans) in range(1, len(posts) + 1)):
                        postid = posts[int(self.user_ans) - 1][3]

                        self.show_comments_of_post(postid)

                else:
                    print('No Post Exists.')


            elif re.match(self.cmdrgx_obj.empty_cmd,self.usercmd) is not None:
                continue


            else:
                print("not a valid command")


    def show_comments_of_post(self,postid):
        comments = self.dbhandler.get_post_comments(
            'text', 'datetime', postid=postid)
        if len(comments):
            for i in range(len(comments)):
                print(
                    '{0}) -----------{1}-----------'.format(i + 1, comments[i][1]))
                print(comments[i][0] + '\n')
        else:
            print('No Comment')


    def show_homepage(self):
        userid, = self.dbhandler.get_user_info(
            "userid", username=self.usercred_obj.username)
        page_info = (self.dbhandler.get_page_info(
            "pagename", "pageid", userid=userid))
        pagename, self.homepagectx = page_info[0]
        self.pagectx = self.homepagectx

        while (True):
            self.usercmd = input("P({0})> ".format(pagename))

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
                        userid, post_text.strip()[:-1], self.pagectx)):
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
                    print('No Post Exists.')

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
                    print('No Post Exists.')

            elif re.match(self.cmdrgx_obj.comment, self.usercmd) is not None:
                page_posts = self.dbhandler.get_posts_by_page_id(
                    '*', destination=self.pagectx)
                if len(page_posts):
                    for i in range(len(page_posts)):
                        print('{0}) -----------{1}-----------'.format(i +
                                                                      1, page_posts[i][3]))
                        post_comment_count = (self.dbhandler.get_post_comments("count(*)", postid=page_posts[i][0]))[0][0]
                        print("📃 {0} comments.\n".format(post_comment_count))
                        print(page_posts[i][2]+'\n')
                    while True:
                        self.user_ans = re.sub("\s*", "", input("📃 Which Post Do You Want To Comment? "))

                        if self.user_ans.isdigit() and (int(self.user_ans) in range(1, len(page_posts)+1)):
                            postid = page_posts[int(self.user_ans)-1][0]

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
                    print('No Post Exists.')

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

            elif re.match(self.cmdrgx_obj.enter_group,self.usercmd) is not None:

                grp_name=(self.usercmd.strip()).split()[1]

                all_groups= self.dbhandler.get_groups_of_user(userid)

                # filtering all groups based on grp_name
                all_wanted_groups=[grp for grp in all_groups if grp[0]==grp_name]


                if len(all_wanted_groups)==0:
                    print("You Are Not Member Of Group {0} Anymore".format(grp_name))

                elif len(all_wanted_groups)>1:
                    for i in range(len(all_wanted_groups)):
                        print('{0}.\t{1}\t{2}\n'.format(
                            i + 1, all_wanted_groups[i][0], '😎' if all_wanted_groups[i][1] == userid else ''))
                    while True:
                        self.user_ans = re.sub("\s*", "", input("Which Group Do You Want To Enter? "))
                        if self.user_ans.isdigit() and (int(self.user_ans) in range(1, len(all_wanted_groups) + 1)):
                            groupctx=all_wanted_groups[int(self.user_ans)-1][2]
                            self.show_groupctx(groupctx,grp_name,userid)
                            break
                else:
                    groupctx = all_wanted_groups[0][2]
                    self.show_groupctx(groupctx, grp_name,userid)





            elif re.match(self.cmdrgx_obj.empty_cmd,self.usercmd) is not None:
                continue
            else:
                print("not a valid command")


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




client_obj = FacebookCli()
client_obj.initialize()
client_obj.prompt()
