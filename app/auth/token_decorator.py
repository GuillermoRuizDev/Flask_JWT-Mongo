""" Token requires. """

# Flask
from functools import wraps
from flask import jsonify, request
import jwt

# App
from app.config import Config as config

# decorate token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        print(request.headers)
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            try:
                #jwt.decode(token, config.SECRET_KEY)
                jwt.decode(token, config.SECRET_KEY,'HS256')
            except:
                return jsonify({"status": "fail", "message": "unauthorized 1"}), 401
            return f(*args, **kwargs)
        else:
            return jsonify({"status": "fail", "message": "unauthorized 2"}), 401
    return decorated