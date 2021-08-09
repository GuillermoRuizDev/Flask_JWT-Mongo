""" Endpoint relative to Users """

# Flask
from flask.json import jsonify, request

# Utils
from bson import ObjectId

# App
from app.users import users_blueprint as users
from app.extensions import mongo
from app.utils import PhoneNumberValidation
from app.auth.token_decorator import token_required

# Endpoints
@users.route('/update/<user_id>', methods=['GET','POST'])
@token_required
def update_user(user_id):
    """ Updated users profile for request """
    response = []
    code = 500
    status = "fail"
    message = ""
    try:
        if (request.method == 'POST'):
            data = request.get_json()
            updater = UserProfileUpdate(data["user_profile"])
            print("entró")
            message, res = updater.update(user_id)

            if res:
                #message = "updated successfully"
                status = "successful"
                code = 201
            else:
                #message = "update failed"
                status = "fail"
                code = 404
        else:
            data =  mongo.db.users.find_one({"_id": ObjectId(user_id)})
            data['_id'] = str(data['_id'])
            del data['password']
            if data:
                response = data
                message = "User found"
                status = "successful"
                code = 200
            else:
                message = "User not found"
                status = "fail"
                code = 404
    except Exception as ee:
        message =  str(ee)
        status = "Error"

    return jsonify({"status":status,'data': response, "message":message}), code


@users.route('/get/<int:page>', methods=['GET'])
@token_required
def get_users(page):
    """ Get Users for pages """
    page = int(request.args.get("page", 1))
    per_page = 10  # A const value.

    response = {}
    data = []
    code = 500
    status = "fail"
    message = ""
    try:
        users = mongo.db.users.find().skip(per_page * (page - 1)).limit(per_page)
        users_count = users.count()

        for user in users:
            print(str(user["_id"]))
            if user.get("user_profile") is None :
                data.append({
                    "id" : str(user["_id"]),
                    "email" : user["email"],
                    "user_profile" : []
                })
            else:
                data.append({
                    "id" : str(user["_id"]),
                    "email" : user["email"],
                    "user_profile" : user["user_profile"]
                })
            print(data)

        response = {
            "users": data,
            "_count": users_count,
        }

        #response = [i for i in users]
        #={str(value["_id"]) : value["user_profile"] for key,value  in users}
        code = 200
        status = "Successful"
        message = "Get users successful"
    except Exception as ee:
        message =  str(ee)
        status = "Error"
    return jsonify({"status":status,'data': response, "message":message}), code


# Class
class UserProfileUpdate:
    """ User Profile validate and Update """
    def __init__(self, data):
        self.data = data
        self.response = None
        self.message = "Error update User Profile"

    def update(self, user_id):
        print(self.data["phone_number"])
        phone_validation = PhoneNumberValidation(self.data["phone_number"])
        if phone_validation.validate() :
            self.response = mongo.db.users.update_one(
                {"_id": ObjectId(user_id)},
                { "$set": {
                    "user_profile":{
                        "name": self.data["name"],
                        "last_name": self.data["last_name"],
                        "date_birth": self.data["date_birth"],
                        "phone_number": self.data["phone_number"],
                        "sede": self.data["sede"],
                        "specialization": self.data["specialization"],
                    }
                }
            })
            if self.response :
                self.message = "User update successful"
        else:
            self.message = "User number phone not validate."

        return self.message, self.response