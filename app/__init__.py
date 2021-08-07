from flask import Flask
from app.extensions import mongo, bcrypt

from app.config import Config
from app.auth import auth_blueprint
from app.employee import employee_blueprint


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(employee_blueprint)

    mongo.init_app(app)
    bcrypt.init_app(app)

    return app

#    return app
