
import re
class FacebookCliRegexes:
    def __init__(self):
        self.login='^\s*login\s*$'
        self.signup="^\s*signup\s*$"
        self.exit="^\s*(exit|bye)\s*$"
        self.yes_ans="^\s*y(e(s)?)?\s*$"
        self.no_ans="^\s*n(o)?\s*$"
        self.email="^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$"
        self.date_of_birth="^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[012])-[1-9][0-9][0-9][0-9]\d\d$"
        self.gender="^(male|female)$"

class FacebookUserCredentials:
    def __init__(self,username,password):
        self.username=username
        self.password=password
        self.page_name=str()

a={'1':'2'}
if '1' in a.keys():
    print("ues")



