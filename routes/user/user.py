from models import User
from routes.user import users_v1
from authorization import authorize_route
from before_request import get_attr_from_request_form
from flask import request

def client_id_same_as_authorized_client(client_id):
    from authorization import authorize
    client = authorize(request)
    if client and client.id == client_id:
        return True
    return False


def has_valid_data(request):
    client_id = request.form.get("client_id")
    if not client_id or not client_id_same_as_authorized_client(client_id):
        return False
    user_name = request.form.get("name")
    name_taken = User.load_by_attr("name", user_name)
    if not user_name or name_taken:
        return False
    return True


def create_user(**data):
    user = User(**data)
    user_dict = user.to_dict()
    user.save()
    return user_dict

@users_v1.route("/", methods=["GET", "POST"], strict_slashes=False)
@authorize_route
def all_users():

    if request.method == "POST":
        if not has_valid_data(request):
            return {"message": "Invalid data."}, 404

        client_id = request.form.get("client_id")
        name = request.form.get("name")
        data = {
            "name": name,
            "client_id": client_id
        }
        user_dict = create_user(**data)
        return {"message": "User created successfully.", "user": user_dict}, 201

    users = User.load_all_dict(remove_attr="client_id")
    return {"users": users}, 200


@users_v1.route("/<id>", methods=["GET", "DELETE", "PUT"], strict_slashes=False)
@authorize_route
def users_by_id(id):

    user = User.load_by_id(id)
    if not user:
        return {"message": "Bad user id."}, 404

    user_dict = user.to_dict()

    if request.method == "DELETE":
        user.delete()
        return {"message": "User deleted."}, 204
    
    if request.method == "PUT":
        name = get_attr_from_request_form(request, "name")
        
        if User.load_by_attr("name", name):
            return {"message": "user name taken."}, 400

        user.name = name
        user.save()
        
        return {"message": "user updated."}, 204

    
    return {"message": "OK", "user": user_dict}, 200