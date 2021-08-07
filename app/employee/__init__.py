from flask import Blueprint

employee_blueprint = Blueprint('employee', __name__, url_prefix='/api/v1/employee')# url_prefix='/api/v1/employee')

from app.employee import employee