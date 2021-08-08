""" Utils """
#from werkzeug.security import generate_password_hash#, check_password_hash
import re

regex_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
regex_phone_number = r'(\+519)([0-9]){8}'

# for validating an Email
class EmailValidation:
    def __init__(self, email):
        self.email = email

    def validate(self):
        if re.match(regex_email, self.email):
            return True
        else:
            return False

# for validating phone number
class PhoneNumberValidation:
    def __init__(self, phone_number):
        self.phone_number = phone_number

    def validate(self):
        if re.match(regex_phone_number, self.phone_number):
            return True
        else:
            return False

