from models import User
from routes.user import users_v1
from authorization import authorize_route
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
        user = User(**data)
        user_dict = user.to_dict()
        user.save()
        return {"message": "User created successfully.", "user": user_dict}, 207

    users = User.load_all_dict(remove_attr="client_id")
    return {"users": users}, 200