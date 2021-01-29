
import re
class FacebookCliRegexes:
    def __init__(self):
        self.login='^\s*login\s*$'
        self.signup="^\s*signup\s*$"
        self.exit="^\s*(exit|quit)\s*$"
        self.yes_ans="^\s*y(e(s)?)?\s*$"
        self.no_ans="^\s*n(o)?\s*$"
        self.email="^\s*\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}\s*$"
        self.date_of_birth="^\s*(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[012])-[1-9][0-9][0-9][0-9]\d\d\s*$"
        self.gender="^\s*(male|female)\s*$"
        self.post="^\s*post\s*$"
        self.showpage="^\s*explode\s*$"
        self.visitpage="^\s*visit\s+[a-zA-Z-]+\s*$"
        self.loadhomepage="^\s*home\s*$"
        self.like="^\s*like\s*$"
        self.unlike="^\s*unlike\s*$"
        self.comment="^\s*comment\s*$"
        self.create_group="^\s*newgrp\s*$"
        self.remove_group="^\s*rmgrp\s*$"
        self.leave_group="^\s*leave\s*$"
        self.show_group="^\s*showgrp\s*$"
        self.add_member="^\s*addmem\s*$"
        self.remove_member="^\s*rmmem\s*$"
        self.enter_group="^\s*enter\s+[a-zA-Z-]+\s*$"
        self.empty_cmd="^\s*$"
        self.show_members="^\s*showmem\s*$"
        self.show_group_posts="^\s*showpost\s*$"
        self.show_comments_of_post="^\s*showcmt\s*$"
        self.show_friends="^\s*friends\s*$"
        self.add_friend="^\s*newfriend\s*$"
        self.remove_friend="^\s*rmfriend\s*$"
        self.messenger= "^\s*chat\s*$"
        self.show_chats="^\s*list\s*$"
        self.enter_chat="^\s*enter\s+\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}\s*$"
        self.show_chat_messages="^\s*show\s*$"
        self.send_message_in_chat="^\s*send\s*$"
        self.new_chat_message="^\s*new\s*$"


class FacebookUserCredentials:
    def __init__(self,username,password):
        self.username=username
        self.password=password
        self.page_name=str()





