from werkzeug.security import generate_password_hash#, check_password_hash
import re

# Make a regular expression
# for validating an Email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

class UserLoginValidate:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.status = ""

    def validate(self):
        if re.match(regex, self.username):
            self.generate_password()
        else:
            self.status = "Debe ingresar email"

    def generate_password(self):
        self.__password_hash = generate_password_hash(self.password)

    def get_password(self):
        return self.__password_hash

