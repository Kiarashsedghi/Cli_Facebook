import pymssql
from datetime import datetime


class FacebookDB:

    def __init__(self, server_addr, db_name, username, password):
        self.server_hd = None
        self.server_properties = {
            'host': server_addr,
            'database': db_name,
            'user': username,
            'password': password
        }

    def connect(self):
        '''
        This function connects to database and returns an handler to work with the database
        :return: database handler
        '''
        conn = pymssql.connect(**self.server_properties)
        conn.autocommit(True)
        self.server_hd = conn.cursor()
        return self.server_hd

        # conn = pymssql.connect(server='localhost', port='1433',
        #                        user='SA', password='@1378Alisajad', database='my')
        # conn.autocommit(True)
        # cursor = conn.cursor()
        # self.server_db_handler = curso

    def authenticate_user(self, username, password):
        '''
        This function authenticates user based on username and password user provided
        :param username:
        :param password:
        :return: returns 1 if authentication was successful else 0
        '''

        self.server_hd.execute(
            "select * from users where email='{0}' and password='{1}'".format(username, password))
        if len(self.server_hd.fetchall()) == 0:
            return 0
        return 1

    def is_username_taken(self, username):
        '''
        This function checks whether username is already taken or not
        :param username:
        :return: returns 1 if username has been already taken else 0
        '''
        self.server_hd.execute(
            "select * from users where email='{0}'".format(username))
        if len(self.server_hd.fetchall()) == 0:
            return 0
        return 1

    def create_user(self, **user_info):
        firstname = user_info['firstname']
        lastname = user_info['lastname']
        username = user_info['email']
        password = user_info['password']
        gender = user_info['gender']
        phonenumber = user_info['phonenumber']
        birthdate = user_info['birthdate']

        sql_string = "'{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}'".format(firstname, lastname, birthdate, gender, phonenumber, password,
                                                                                                        username, str(datetime.now()), 'NULL', 'NULL', 'NULL', 'NULL')

        self.server_hd.execute(
            "insert into users values({0})".format(sql_string))

    def update_user_by_username(self, username, **user_info):
        bio = user_info['bio'] if len(user_info['bio']) != 0 else 'NULL'
        currentcityname = user_info['currentcityname'] if len(
            user_info['currentcityname']) != 0 else 'NULL'
        hometownname = user_info['hometownname'] if len(
            user_info['hometownname']) != 0 else 'NULL'
        relationshipstatus = user_info['relationshipstatus'] if len(
            user_info['relationshipstatus']) != 0 else 'NULL'

        sql_string = "set bio='{0}',currentcityname='{1}',hometownname='{2}',relationshipstatus='{3}'".format(
            bio, currentcityname, hometownname, relationshipstatus)
        self.server_hd.execute(
            "update users {0} where email='{1}'".format(sql_string, username))

    def get_user_info(self, *args, **kwargs):
        args = [str(e) for e in args]
        columns = " , ".join(args)
        conditions = str()
        for k, v in kwargs.items():
            if k.lower() == "userid":
                conditions += (k+"="+str(v)+" ")
            else:
                conditions += (k+"='"+str(v)+"' ")

        conditions = " and ".join(conditions.split())
        conditions = conditions.replace("username", "email")

        self.server_hd.execute(
            "select {0} from users where {1}".format(columns, conditions))
        query_result = self.server_hd.fetchall()

        if len(query_result) != 0:
            return query_result[0]

        return None

    def get_page_info(self, *args, **kwargs):
        args = [str(e) for e in args]
        columns = " , ".join(args)
        conditions = str()
        for k, v in kwargs.items():
            if k.lower() in "pageid userid":
                conditions += (k+"="+str(v)+" ")
            else:
                conditions += (k+"='"+str(v)+"' ")

        conditions = " and ".join(conditions.split())

        self.server_hd.execute(
            "select {0} from pages where {1}".format(columns, conditions))
        query_result = self.server_hd.fetchall()

        return query_result

    def create_new_post(self, uid, text, pageId, type):
        if type == "Page":

            sql_string = "{0},'{1}','{2}',{3}".format(
                uid, text, str(datetime.now()), pageId)
            try:
                self.server_hd.execute(
                    "insert into posts values({0})".format(sql_string))
                return 1
            except:
                return 0

    def get_posts_by_page_id(self, *args, **kwargs):
        args = [str(e) for e in args]
        columns = " , ".join(args)
        conditions = str()
        for k, v in kwargs.items():
            if k.lower() in "postid userid destination":
                conditions += (k + "=" + str(v) + " ")
            else:
                conditions += (k + "='" + str(v) + "' ")

        conditions = " and ".join(conditions.split())

        self.server_hd.execute(
            "select {0} from posts where {1}".format(columns, conditions))
        query_result = self.server_hd.fetchall()

        return query_result

    def like_post(self, postid, userid):
        sql_string = "{0},{1},'{2}'".format(
            postid, userid, str(datetime.now()))
        try:
            self.server_hd.execute(
                "insert into postlikes values ({0})".format(sql_string))
            return 1
        except:
            return 0

    def comment_post(self, postid, userid, text):
        sql_string = "{0},{1},'{2}','{3}'".format(
            postid, userid, text, str(datetime.now()))
        try:
            self.server_hd.execute(
                "insert into comments values ({0})".format(sql_string))
            return 1
        except:
            return 0

    def dislike_post(self, postid, userid):
        sql_string = "postid={0} and userid={1}".format(
            postid, userid)
        try:
            self.server_hd.execute(
                "delete from postlikes where ({0})".format(sql_string))
            return 1
        except:
            return 0

    def get_post_comments(self, *args, ** kwargs):
        args = [str(e) for e in args]
        columns = " , ".join(args)
        conditions = str()
        for k, v in kwargs.items():
            if k.lower() in "commentid postid userid":
                conditions += (k + "=" + str(v) + " ")
            else:
                conditions += (k + "='" + str(v) + "' ")

        conditions = " and ".join(conditions.split())

        self.server_hd.execute(
            "select {0} from comments where {1}".format(columns, conditions))
        query_result = self.server_hd.fetchall()
        return query_result

    def get_post_likes(self, *args, ** kwargs):
        args = [str(e) for e in args]
        columns = " , ".join(args)
        conditions = str()
        for k, v in kwargs.items():
            if k.lower() in "postid userid":
                conditions += (k + "=" + str(v) + " ")
            else:
                conditions += (k + "='" + str(v) + "' ")

        conditions = " and ".join(conditions.split())

        self.server_hd.execute(
            "select {0} from postLikes where {1}".format(columns, conditions))
        query_result = self.server_hd.fetchall()

        return query_result

    def create_new_page(self, username, page_name=None, category=None):

        userid, firstname, lastname = self.get_user_info(
            "userid", "firstname", "lastname", username=username)

        if page_name is None:
            page_name = firstname+"-"+lastname

        if category is None:
            category = "Regular"

        self.server_hd.execute(
            "select top 1 PageID from pages order by PageID desc ")
        query_result = self.server_hd.fetchall()
        page_id = 0
        if len(query_result) != 0:
            page_id = query_result[0][0]
            page_id += 2

        sql_string = "{0},{1},'{2}','{3}','{4}',{5},'{6}','{7}'".format(
            page_id, userid, page_name, category, 'NULL', '0', 'NULL', str(datetime.now()))
        status = self.server_hd.execute(
            "insert into pages values({0})".format(sql_string))

    def create_new_group(self, adminid, groupname, group_description):
        self.server_hd.execute(
            "select top 1 GroupID from Groups order by GroupID desc ")
        query_result = self.server_hd.fetchall()
        group_id = 1
        if len(query_result) != 0:
            group_id = query_result[0][0]
            group_id += 2
        now_date = str(datetime.now())
        sql_string_group = "{0},{1},'{2}','{3}','{4}'".format(
            group_id, adminid, groupname, group_description, now_date)
        try:
            self.server_hd.execute(
                "insert into groups values({0})".format(sql_string_group))
            if(self.add_member_to_group(group_id, adminid, now_date)):
                return 1
            return 0
        except:
            return 0

    def add_member_to_group(self, groupid, userid, nowdate=None):
        sql_string_get_members = 'groupid={0} and userid={1}'.format(groupid,userid)
        self.server_hd.execute(
                "select * from  groupmembers where ({0})".format(sql_string_get_members))
        query_result = self.server_hd.fetchall()
        if (len(query_result)):
            return 0
        now_date = str(datetime.now()) if nowdate is None else nowdate
        sql_string = "{0},{1},'{2}'".format(
            groupid, userid, now_date)
        try:
            self.server_hd.execute(
                "insert into groupmembers values({0})".format(sql_string))
            return 1
        except:
            return 0

    def get_groups_info(self, *args, ** kwargs):
        args = [str(e) for e in args]
        columns = " , ".join(args)
        conditions = str()
        for k, v in kwargs.items():
            if k.lower() in "groupid admin":
                conditions += (k + "=" + str(v) + " ")
            else:
                conditions += (k + "='" + str(v) + "' ")

        conditions = " and ".join(conditions.split())

        self.server_hd.execute(
            "select {0} from groups where {1}".format(columns, conditions))
        query_result = self.server_hd.fetchall()

        return query_result

    def get_groups_of_user(self, userid):
        self.server_hd.execute(
            "select g.GroupName,g.Admin,g.groupID from GroupMembers gm inner join groups g on gm.GroupID=g.GroupID where gm.UserID={0}".
            format(userid))
        query_result = self.server_hd.fetchall()
        return query_result
