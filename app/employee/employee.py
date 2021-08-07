from flask.json import jsonify
from app.employee import employee_blueprint as employee

@employee.route('/login', methods=['GET', 'POST'])
def list_empleyee():
    return jsonify({"status": "Successful", "message":"Empleoyee",'data':""}), 200


@employee.route('/', methods=['GET'])
def list_empleyee_2():
    return "Hola"