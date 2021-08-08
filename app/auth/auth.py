""" Authentication users. """

# Flask
from flask import jsonify, request
import jwt
from datetime import datetime, timedelta
from bson import ObjectId
from functools import wraps

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
            password_hashed = SignupValidate(data['password'])
            #data['password'] = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            data['password'] = password_hashed.get_password_hash()
            data['created'] = datetime.now()

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


# Endpoint to update login user with
@auth.route('/update/<user_id>', methods=['GET','POST'])
def update_login(user_id):
    data = {}
    code = 500
    message = ""
    status = "fail"
    try:
        if (request.method == 'POST'):
            data = request.get_json()
            sign_update = SignupValidate(data["new_password"])
            res = mongo.db.users.update_one(
                {"_id": ObjectId(user_id)},
                { "$set":
                    {'title': sign_update.get_password_hash(),
                     'created': datetime.now()
                     }
                }
            )
            if res:
                message = "updated successfully"
                status = "successful"
                code = 201
            else:
                message = "update failed"
                status = "fail"
                code = 404
        else:
            data =  mongo.db.users.find_one({"_id": ObjectId(user_id)})
            data['_id'] = str(data['_id'])

            if data:
                del data['password']
                message = "item found"
                status = "successful"
                code = 200
            else:
                message = "update failed"
                status = "fail"
                code = 404
    except Exception as ee:
        message =  str(ee)
        status = "Error"

    return jsonify({"status": status, "message":message,'data': data}), code


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

def tokenReq(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            try:
                jwt.decode(token, config.SECRET_KEY)
            except:
                return jsonify({"status": "fail", "message": "unauthorized"}), 401
            return f(*args, **kwargs)
        else:
            return jsonify({"status": "fail", "message": "unauthorized"}), 401
    return decorated