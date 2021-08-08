from flask import Blueprint

users_blueprint = Blueprint('employee', __name__, url_prefix='/api/v1/users')# url_prefix='/api/v1/employee')

from app.users import users