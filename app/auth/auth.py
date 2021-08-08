""" Authentication users. """

# Flask
from flask import jsonify, request
import jwt
from datetime import datetime, timedelta

# App
from app.extensions import mongo , bcrypt
from app.config import Config as config
from app.auth import auth_blueprint as auth


#Endpoints

@auth.route('/signup', methods=['POST'])
def save_user():
    """ EndPoint create user. """
    message = ""
    code = 500
    status = "fail"
    try:
        data = request.get_json()
        check = mongo.db.users.find_one({"email": data['email']})
        if check:
            message = "user with that email exists"
            code = 401
            status = "fail"
        else:
            # hashing the password so it's not stored in the db as it was
            password_hashed = SignupValidate(data['password'])
            #data['password'] = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            data['password'] = password_hashed.get_password_hash()
            data['created'] = datetime.now()

            #this is bad practice since the data is not being checked before insert
            res = mongo.db.users.insert_one(data)
            if res.acknowledged:
                status = "successful"
                message = "user created successfully"
                code = 201
    except Exception as ex:
        message = f"{ex}"
        status = "fail"
        code = 500
    return jsonify({'status': status, "message": message}), code


# EndPoint to login user
@auth.route('/login', methods=['POST'])
def login():
    """ Endpoint login user """
    message = ""
    res_data = {}
    code = 500
    status = "fail"
    try:
        data = request.get_json()
        print(f'{data["email"]}')
        user = mongo.db.users.find_one({"email": f'{data["email"]}'})

        if user:
            user['_id'] = str(user['_id'])
            password_hashed = SignupValidate(data['password'])

            #if user and bcrypt.check_password_hash(user['password'], data['password']):
            if user and password_hashed.check_password(user['password']):
                time = datetime.utcnow() + timedelta(hours=24)
                token_gen = TokenGenerate

                token = token_gen.generate(user,time)

                del user['password']

                message = f"user authenticated"
                code = 200
                status = "successful"
                res_data['token'] = token
                res_data['user'] = user

            else:
                message = "wrong password"
                code = 401
                status = "fail"
        else:
            message = "invalid login details"
            code = 401
            status = "fail"

    except Exception as ex:
        message = f"{ex}"
        code = 500
        status = "fail"
    return jsonify({'status': status, "data": res_data, "message":message}), code


# Class

class SignupValidate:
    def __init__(self, password):
        self.password = password

    def get_password_hash(self):
        return bcrypt.generate_password_hash(self.password).decode('utf-8')

    def check_password(self, db_password):
        return bcrypt.check_password_hash(db_password, self.password)


class TokenGenerate:
    def generate(user, time):
        token = jwt.encode({
                        "user": {
                            "email": f"{user['email']}",
                            "id": f"{user['_id']}",
                        },
                        "exp": time
                    },config.SECRET_KEY)
        return token