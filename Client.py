from Server import *
from lib import *
import re
from time import sleep
from datetime import datetime

from os import system
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
        self.homepagename = str()
        self.user_ans = str()

    def get_userpass(self):
        '''
        Prompting and asks users for their username and password
        :return:(username,password)
        '''
        username = input("👱🏻‍♂️ Username: ")
        password = getpass("🔑 Password: ")
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
            if self.dbhandler.does_username_exist(username):
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

    def print_group_posts(self, index, post, liked_count, comment_count):

        print('-------------------------')
        print("{0}. By {1} On {2}".format(index + 1, post[0], post[2]))
        print("liked by {0} ❤️ users".format(liked_count))
        print("{0} 📃 comments".format(comment_count))
        print("🗒: \n")
        print(post[1])

    def show_groupctx(self, groupid, grp_name, userid):

        while True:
            self.usercmd = input("G({0})> ".format(grp_name))

            if re.match(self.cmdrgx_obj.exit, self.usercmd) is not None:
                print("exit from group!")
                break

            elif re.match(self.cmdrgx_obj.show_members, self.usercmd) is not None:
                members = self.dbhandler.get_members_of_group(groupid)
                if len(members) == 0:
                    print("No Member Exist In This Group")
                else:
                    for i in range(len(members)):
                        member_userid = self.dbhandler.get_user_info(
                            "userid", username=members[i][0])[0]

                        if self.dbhandler.is_user_admin_of_group(member_userid, groupid):
                            # TODO show who is admin
                            print("{0}. {1} 😎".format(i + 1, members[i][0]))
                        else:
                            print("{0}. {1}".format(i + 1, members[i][0]))

            elif re.match(self.cmdrgx_obj.remove_member, self.usercmd) is not None:
                if self.dbhandler.is_user_admin_of_group(userid, groupid):

                    members = self.dbhandler.get_members_of_group(groupid)

                    if len(members) == 0:
                        print("No Member Exist In This Group")
                    else:
                        for i in range(len(members)):
                            member_userid = self.dbhandler.get_user_info(
                                "userid", username=members[i][0])[0]

                            if self.dbhandler.is_user_admin_of_group(member_userid, groupid):
                                # TODO show who is admin
                                print("{0}. {1} 😎".format(
                                    i + 1, members[i][0]))
                            else:
                                print("{0}. {1}".format(i + 1, members[i][0]))

                        while True:
                            self.user_ans = re.sub(
                                "\s*", "", input("⚠️ Which Member Do You Want To Remove? "))
                            if self.user_ans.isdigit() and (int(self.user_ans) in range(1, len(members) + 1)):
                                member_username = members[int(
                                    self.user_ans) - 1][0]
                                member_userid = self.dbhandler.get_user_info(
                                    "userid", username=member_username)[0]
                                print('Deleting...')
                                sleep(1)
                                if member_userid == userid:
                                    print(
                                        "❌ You Cannot Delete Yourself, You Are Admin")
                                else:
                                    if self.dbhandler.remove_user_from_group(groupid, member_userid):
                                        print("✅ Member Removed Successfully")
                                    else:
                                        print('❌ Member Removal Failed')
                                break

                else:
                    print(
                        "❌ Your Are Not Admin Of The Group {0}".format(grp_name))

            elif re.match(self.cmdrgx_obj.leave_group, self.usercmd) is not None:
                if not self.dbhandler.is_user_admin_of_group(userid, groupid):
                    print('Leaving...')
                    sleep(1)
                    if self.dbhandler.leave_group(groupid, userid):
                        print("✅ You Left The Group Successfully")
                        return
                    else:
                        print("❌ Leaving Group Failed")
                else:
                    print(
                        "❌ You Are Admin Of Group {0}, You Cannot Leave".format(grp_name))

            elif re.match(self.cmdrgx_obj.post, self.usercmd) is not None:
                post_text = str()
                print('🗒 Enter Your Post Content:')
                temp = str()
                while len(temp) == 0 or temp != ".":
                    temp = (input()).strip()

                    post_text += temp + "\n"

                print("Creating Post...")
                sleep(1)
                if (self.dbhandler.create_new_post(
                        userid, post_text.strip()[:-1], groupid)):
                    print("✅ Post Created.")
                else:
                    print('❌ Post creation failed ')

            elif re.match(self.cmdrgx_obj.show_group_posts, self.usercmd) is not None:
                posts = self.dbhandler.get_posts_of_group(groupid)
                if len(posts) == 0:
                    print("No One Has Posted Anything Yet")

                else:
                    for i in range(len(posts)):
                        post_like_count = (self.dbhandler.get_post_likes(
                            "count(*)", postid=posts[i][3]))[0][0]
                        post_comment_count = (self.dbhandler.get_post_comments(
                            "count(*)", postid=posts[i][3]))[0][0]
                        self.print_group_posts(
                            i, posts[i], post_like_count, post_comment_count)

            elif re.match(self.cmdrgx_obj.like, self.usercmd) is not None:
                posts = self.dbhandler.get_posts_of_group(groupid)

                if len(posts):
                    for i in range(len(posts)):
                        post_like_count = (self.dbhandler.get_post_likes(
                            "count(*)", postid=posts[i][3]))[0][0]
                        post_comment_count = (self.dbhandler.get_post_comments(
                            "count(*)", postid=posts[i][3]))[0][0]
                        self.print_group_posts(
                            i, posts[i], post_like_count, post_comment_count)

                    while True:
                        self.user_ans = re.sub(
                            "\s*", "", input("❤️ Which Post Do You Like? "))
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
                        post_like_count = (self.dbhandler.get_post_likes(
                            "count(*)", postid=posts[i][3]))[0][0]
                        post_comment_count = (self.dbhandler.get_post_comments(
                            "count(*)", postid=posts[i][3]))[0][0]
                        self.print_group_posts(
                            i, posts[i], post_like_count, post_comment_count)

                    while True:
                        self.user_ans = re.sub(
                            "\s*", "", input("📃 Which Post Do You Want To Comment? "))

                        if self.user_ans.isdigit() and (int(self.user_ans) in range(1, len(posts) + 1)):
                            postid = posts[int(self.user_ans) - 1][3]

                            comment_text = str()
                            temp = str()
                            print('📃 Enter Your Comment:')
                            while len(temp) == 0 or temp != ".":
                                temp = (input()).strip()
                                comment_text += temp + "\n"

                            comment_text = comment_text.strip()[:-1]

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
                    self.user_ans = re.sub(
                        "\s*", "", input("📃 Which Post Do You Want To See Comments? "))

                    if self.user_ans.isdigit() and (int(self.user_ans) in range(1, len(posts) + 1)):
                        postid = posts[int(self.user_ans) - 1][3]

                        self.show_comments_of_post(postid)

                else:
                    print('No Post Exists.')

            elif re.match(self.cmdrgx_obj.empty_cmd, self.usercmd) is not None:
                continue

            else:
                print("Not A Valid Command")

    def show_comments_of_post(self, postid):
        comments = self.dbhandler.get_post_comments(
            'text', 'datetime', postid=postid)
        if len(comments):
            for i in range(len(comments)):
                print(
                    '{0}) -----------{1}-----------'.format(i + 1, comments[i][1]))
                print(comments[i][0] + '\n')
        else:
            print('No Comment')

    def show_chat_context(self, username, userid, peer_userid):

        while (True):
            self.usercmd = input("C({0})> ".format(username))

            if re.match(self.cmdrgx_obj.exit, self.usercmd) is not None:
                print("Exit From Chat!")
                return

            elif re.match(self.cmdrgx_obj.show_chat_messages, self.usercmd) is not None:

                incoming_chats = self.dbhandler.get_messages_info("text", "datetime", touserid=userid,
                                                                  fromuserid=peer_userid)
                outgoing_chats = self.dbhandler.get_messages_info("text", "datetime", touserid=peer_userid,
                                                                  fromuserid=userid)

                incoming_chats = [('i', *e) for e in incoming_chats]
                outgoing_chats = [('o', *e) for e in outgoing_chats]

                all_chats = [*incoming_chats, *outgoing_chats]

                # sort by datetime
                all_chats = sorted(all_chats, key=lambda x: x[2])
                if len(all_chats) == 0:
                    print("No Message Yet")
                else:
                    for chat in all_chats:
                        if chat[0] == 'o':
                            for index, line in enumerate(chat[1].split("\n")):
                                if line.strip():
                                    if index == 0:
                                        print("\t\t\t\t\t📤 {0}".format(line))
                                    else:
                                        print("\t\t\t\t\t   {0}".format(line))
                        else:
                            for index, line in enumerate(chat[1].split("\n")):
                                if line.strip():
                                    if index == 0:
                                        print("📥 {0}".format(line))
                                    else:
                                        print("   {0}".format(line))

            elif re.match(self.cmdrgx_obj.send_message_in_chat, self.usercmd) is not None:
                message_text = str()
                print('✉️ Enter Your Message Content:')
                temp = str()
                while len(temp) == 0 or temp != ".":
                    temp = (input()).strip()
                    message_text += temp + "\n"

                # TODO emoji
                if self.dbhandler.send_message_in_chat(userid, peer_userid, message_text.strip()[:-1]):
                    print("✅ Your Message Sent Successfully")
                else:
                    print("❌ Your Message Not Sent")

            elif re.match(self.cmdrgx_obj.empty_cmd, self.usercmd) is not None:
                continue
            else:
                print("Not A Valid Command")

    def run_messanger(self, userid, username):

        while (True):
            self.usercmd = input("M({0})> ".format(username))

            if re.match(self.cmdrgx_obj.exit, self.usercmd) is not None:
                print("Exit From Messenger!")
                return

            elif re.match(self.cmdrgx_obj.show_chats, self.usercmd) is not None:

                chatlist = self.dbhandler.get_users_have_chats_with(userid)

                if len(chatlist) == 0:
                    print("No Message Yet")

                else:
                    for i in range(len(chatlist)):
                        print("💬 {0}. {1}".format(i+1, chatlist[i][0]))

            elif re.match(self.cmdrgx_obj.new_chat_message, self.usercmd) is not None:
                peer_username = input("💬 Who Do You Want To Chat With? ")

                if self.dbhandler.does_username_exist(peer_username):
                    chatlist = self.dbhandler.get_users_have_chats_with(userid)
                    # check whether we had chat with peer_username or not
                    if peer_username in [e[0] for e in chatlist]:
                        print("⚠️ You Have Already a Chat Session With {0}".format(
                            peer_username))

                    peer_userid = self.dbhandler.get_user_info(
                        "userid", username=peer_username)[0]
                    self.show_chat_context(peer_username, userid, peer_userid)

                    pass
                else:
                    print("❌ Username {0} Does Not Exist".format(
                        peer_username))

                pass

            elif re.match(self.cmdrgx_obj.enter_chat, self.usercmd) is not None:

                username = (self.usercmd.strip()).split()[-1]

                user_id_tuple = self.dbhandler.get_user_info(
                    "userid", username=username)

                if user_id_tuple:
                    self.show_chat_context(username, userid, user_id_tuple[0])

                else:
                    print("❌ Username {0} Does Not Exist".format(username))

            elif re.match(self.cmdrgx_obj.empty_cmd, self.usercmd) is not None:
                continue
            else:
                print("Not A Valid Command")

    def show_homepage(self):
        userid, = self.dbhandler.get_user_info(
            "userid", username=self.usercred_obj.username)
        page_info = (self.dbhandler.get_page_info(
            "pagename", "pageid", userid=userid))
        self.homepagename, self.homepagectx = page_info[0]
        self.pagectx = self.homepagectx
        pagename = self.homepagename

        while (True):
            self.usercmd = input("P({0})> ".format(pagename))

            if re.match(self.cmdrgx_obj.exit, self.usercmd) is not None:
                print("Exit From Account!")
                return

            elif (re.match(self.cmdrgx_obj.post, self.usercmd) is not None) and self.pagectx == self.homepagectx:
                post_text = str()
                print('🗒 Enter Your Post Content:')
                temp = str()
                while len(temp) == 0 or temp != ".":
                    temp = (input()).strip()
                    post_text += temp+"\n"

                print("Creating Post...")
                sleep(1)
                if(self.dbhandler.create_new_post(
                        userid, post_text.strip()[:-1], self.pagectx)):
                    print("✅ Post Created")
                else:
                    print('❌ Post creation failed ')

            elif re.match(self.cmdrgx_obj.showpage, self.usercmd) is not None:
                page_contents = self.dbhandler.get_page_info(
                    "*", pageid=self.pagectx)
                page_posts = self.dbhandler.get_posts_by_page_id(
                    "*", destination=self.pagectx)
                # print(page_contents, page_posts)
                page_info = page_contents[0]
                page_name = page_info[2]

                print('------------{0}------------\n\n'.format(page_name))
                if len(page_posts):
                    for i in range(len(page_posts)):
                        print('{0})-----------{1}-----------'.format(i +
                                                                     1, page_posts[i][3]))
                        post_like_count = (self.dbhandler.get_post_likes(
                            "count(*)", postid=page_posts[i][0]))[0][0]
                        print("❤️ liked by {0} users\n".format(
                            post_like_count))
                        print('🗒: ')
                        print(page_posts[i][2]+'\n')

            elif re.match(self.cmdrgx_obj.like, self.usercmd) is not None:
                page_posts = self.dbhandler.get_posts_by_page_id(
                    '*', destination=self.pagectx)
                if len(page_posts):
                    for i in range(len(page_posts)):
                        print('{0})-----------{1}-----------'.format(i +
                                                                     1, page_posts[i][3]))
                        post_like_count = (self.dbhandler.get_post_likes(
                            "count(*)", postid=page_posts[i][0]))[0][0]
                        print("❤️ liked by {0} users\n".format(
                            post_like_count))
                        print('🗒: ')
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

            elif re.match(self.cmdrgx_obj.unlike, self.usercmd) is not None:
                page_posts = self.dbhandler.get_posts_by_page_id(
                    '*', destination=self.pagectx)
                if len(page_posts):
                    for i in range(len(page_posts)):
                        print('{0}) -----------{1}-----------'.format(i +
                                                                      1, page_posts[i][3]))
                        post_like_count = (self.dbhandler.get_post_likes(
                            "count(*)", postid=page_posts[i][0]))[0][0]
                        print("❤️ liked by {0} users\n".format(
                            post_like_count))
                        print(page_posts[i][2]+'\n')
                        # Todo : likes count
                    while True:
                        self.user_ans = re.sub(
                            "\s*", "", input("💔 Which Post Do You Unlike? "))
                        if self.user_ans.isdigit() and (int(self.user_ans) in range(1, len(page_posts)+1)):
                            postid = page_posts[int(
                                self.user_ans)-1][0]
                            if self.dbhandler.dislike_post(postid, userid):
                                print("✅ Post Unliked")
                            else:
                                print('❌ Post Unlike failed ')
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
                        post_comment_count = (self.dbhandler.get_post_comments(
                            "count(*)", postid=page_posts[i][0]))[0][0]
                        print("📃 {0} comments.\n".format(post_comment_count))
                        print(page_posts[i][2]+'\n')
                    while True:
                        self.user_ans = re.sub(
                            "\s*", "", input("📃 Which Post Do You Want To Comment? "))

                        if self.user_ans.isdigit() and (int(self.user_ans) in range(1, len(page_posts)+1)):
                            postid = page_posts[int(self.user_ans)-1][0]

                            comment_text = str()
                            temp = str()
                            print('📃 Enter Your Comment:')
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
                destination_page = (self.usercmd).split()[1]
                query_result = self.dbhandler.get_page_info(
                    "pageid", pagename=destination_page)

                if len(query_result) == 0:
                    print("❌ Page {0} does not exist anymore".format(
                        destination_page))
                elif len(query_result) == 1:
                    pagename = destination_page
                    self.pagectx = query_result[0][0]
                else:
                    for i in range(len(query_result)):
                        print("📑 {0}. {1} {2}".format(
                            i+1, destination_page, query_result[i][0]))

                    while True:
                        self.user_ans = re.sub(
                            "\s*", "", input("📑 which page do you want to visit? "))
                        if self.user_ans.isdigit() and (int(self.user_ans) in range(1, len(query_result)+1)):
                            pagename = destination_page
                            self.pagectx = query_result[int(
                                self.user_ans)-1][0]
                            break

            elif re.match(self.cmdrgx_obj.loadhomepage, self.usercmd) is not None:
                pagename = self.homepagename
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

            elif re.match(self.cmdrgx_obj.remove_group, self.usercmd) is not None:

                groups = self.dbhandler.get_groups_of_user(userid)

                if len(groups) == 0:
                    print("No Group To Remove")

                else:
                    for i in range(len(groups)):
                        print('{0}.\t{1}\t{2}\n'.format(
                            i + 1, groups[i][0], '😎' if groups[i][1] == userid else ''))

                    while True:
                        self.user_ans = re.sub(
                            "\s*", "", input("⚠️ Which Group Do You Want To Remove? "))
                        if self.user_ans.isdigit() and (int(self.user_ans) in range(1, len(groups) + 1)):
                            group_id = groups[int(self.user_ans) - 1][2]
                            grp_name = groups[int(self.user_ans) - 1][0]

                            print('Removing Group...')
                            sleep(1)

                            if self.dbhandler.is_user_admin_of_group(userid, group_id):
                                if self.dbhandler.remove_group(group_id):
                                    print(
                                        "✅ Group {0} Removed Successfully".format(grp_name))
                                else:
                                    print("❌ Group Removal Failed")
                            else:
                                print(
                                    "❌ You Are Not Admin Of This Group, You Cannot Remove This Group")
                            break

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
                            "\s*", "", input("👨‍👩‍👦‍👦 Which Group Do You Want To Add Member To? "))
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

            elif re.match(self.cmdrgx_obj.enter_group, self.usercmd) is not None:

                grp_name = (self.usercmd.strip()).split()[1]

                all_groups = self.dbhandler.get_groups_of_user(userid)

                # filtering all groups based on grp_name
                all_wanted_groups = [
                    grp for grp in all_groups if grp[0] == grp_name]

                if len(all_wanted_groups) == 0:
                    print(
                        "❌ You Are Not Member Of Group {0} Anymore".format(grp_name))

                elif len(all_wanted_groups) > 1:
                    for i in range(len(all_wanted_groups)):
                        print('{0}.\t{1}\t{2}\n'.format(
                            i + 1, all_wanted_groups[i][0], '😎' if all_wanted_groups[i][1] == userid else ''))
                    while True:
                        self.user_ans = re.sub(
                            "\s*", "", input("👨‍👩‍👦‍👦 Which Group Do You Want To Enter? "))
                        if self.user_ans.isdigit() and (int(self.user_ans) in range(1, len(all_wanted_groups) + 1)):
                            groupctx = all_wanted_groups[int(
                                self.user_ans)-1][2]
                            self.show_groupctx(groupctx, grp_name, userid)
                            break
                else:
                    groupctx = all_wanted_groups[0][2]
                    self.show_groupctx(groupctx, grp_name, userid)

            elif re.match(self.cmdrgx_obj.show_friends, self.usercmd) is not None:
                friends = self.dbhandler.get_friends_of_user(userid)
                if len(friends) == 0:
                    print("No Friend")
                else:
                    for i in range(len(friends)):
                        print("🤜🤛 {0}. {1}".format(i+1, friends[i][0]))

            elif re.match(self.cmdrgx_obj.add_friend, self.usercmd) is not None:

                friend_username = input("🥸 Enter Friend Username: ")

                print('Adding Friendship...')
                sleep(1)
                if self.dbhandler.does_username_exist(friend_username):
                    if self.dbhandler.create_new_friendship(userid, friend_username):
                        print("✅ Friendship Added Successfully")
                    else:
                        print("❌ Friendship Addition Failed")
                else:
                    print("Username Entered Does Not Exist")

            elif re.match(self.cmdrgx_obj.remove_friend, self.usercmd) is not None:
                friends = self.dbhandler.get_friends_of_user(userid)
                if len(friends) == 0:
                    print("No Friend")
                else:
                    for i in range(len(friends)):
                        print("🤜🤛 {0}. {1}".format(i + 1, friends[i][0]))

                    while True:
                        self.user_ans = re.sub(
                            "\s*", "", input("Which Friend Do You Want To Unfollow? "))
                        print('Removing Friendship...')
                        sleep(1)
                        if self.user_ans.isdigit() and (int(self.user_ans) in range(1, len(friends)+1)):
                            friendid = friends[int(self.user_ans)-1][1]

                            if self.dbhandler.remove_friendship(userid, friendid):
                                print("✅ Friendship With {0} Removed Successfully".format(
                                    friends[int(self.user_ans)-1][0]))

                            else:
                                print("❌ Friendship Removal Failed")

                            break

            elif re.match(self.cmdrgx_obj.messenger, self.usercmd) is not None:
                self.run_messanger(userid, self.usercred_obj.username)

            elif re.match(self.cmdrgx_obj.empty_cmd, self.usercmd) is not None:
                continue
            elif re.match(self.cmdrgx_obj.profile, self.usercmd) is not None:
                system("python3 ./profile.py " + str(userid))

            else:
                print("Not A Valid Command")

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
                    print(
                        "------------⭐️ Welcome {0} ⭐️------------".format(self.usercred_obj.username))
                    self.show_homepage()
                else:
                    print("❌ Username Or Password Is Incorrect")

            # Create new user
            elif re.match(self.cmdrgx_obj.signup, self.usercmd) is not None:
                self.signup()
                self.show_homepage()

            elif re.match(self.cmdrgx_obj.exit, self.usercmd) is not None:
                print("Bye! See You Later")
                exit(0)


client_obj = FacebookCli()
client_obj.initialize()
client_obj.prompt()
