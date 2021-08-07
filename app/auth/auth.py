from flask import jsonify, request
from app.extensions import mongo , bcrypt
from datetime import datetime, timedelta
from app.config import Config as config
import jwt
#from app.forms import LoginForm

from app.auth import auth_blueprint as auth


@auth.route('/signup', methods=['POST'])
def save_user():
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
            data['password'] = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            data['created'] = datetime.now()

            #this is bad practice since the data is not being checked before insert
            res = mongo.db["users"].insert_one(data)
            if res.acknowledged:
                status = "successful"
                message = "user created successfully"
                code = 201
    except Exception as ex:
        message = f"{ex}"
        status = "fail"
        code = 500
    return jsonify({'status': status, "message": message}), code
