
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
        self.dislike="^\s*dislike\s*$"
        self.comment="^\s*comment\s*$"
        self.create_group="^\s*newgrp*\s*$"
        self.show_group="^\s*showgrp*\s*$"
        self.add_member="^\s*addmem*\s*$"
        self.enter_group="^\s*enter\s+[a-zA-Z-]+\s*$"
        self.empty_cmd="^\s*$"
        self.show_members="^\s*showmem*\s*$"
        self.show_group_posts="^\s*showpost*\s*$"
        self.show_comments_of_post="^\s*showcmt*\s*"


class FacebookUserCredentials:
    def __init__(self,username,password):
        self.username=username
        self.password=password
        self.page_name=str()



