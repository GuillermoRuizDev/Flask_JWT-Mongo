from flask.json import jsonify
from app.users import users_blueprint as users

@users.route('/login', methods=['GET', 'POST'])
def list_empleyee():
    return jsonify({"status": "Successful", "message":"Empleoyee",'data':""}), 200


@users.route('/users/<str:id>', methods=['GET'])
def get_user():
    response = []
    code = 500
    status = "fail"
    message = ""
    return jsonify({"status":status,'data': response, "message":message}), code