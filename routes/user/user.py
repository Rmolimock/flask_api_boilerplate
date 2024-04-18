from routes.user import users_v1
from authorization import authorized_client


@users_v1.route("/", methods=["POST"], strict_slashes=False)
@authorized_client
def create_user():
    """
    Create a user
    """
    from flask import request
    from models import User

    name = request.form.get("name")
    if not name:
        return "User name is required\n", 400

    try:
        user = User(**{"name": name})
    except Exception as e:
        return str(e), 500

    if not user:
        return "Failed to create user\n", 500

    user_dict = user.to_dict()
    user.save()

    return user_dict, 201


@users_v1.route("/", methods=["GET"], strict_slashes=False)
@authorized_client
def all_users():
    """
    Get all users
    """
    from models import User

    users = User.load_all_dict()
    if not users:
        return [], 200

    return users, 200


@users_v1.route("/<id>", methods=["GET", "DELETE", "PUT"], strict_slashes=False)
@authorized_client
def get_by_id(id):
    """
    Get, update, or delete a user by id
    """
    from flask import request
    from models import User

    user = User.load_by_id(id)
    if not user:
        return "Not found. Invalid user ID.\n", 404
    
    if request.method == "GET":
        return user.to_dict(), 200

    if request.method == "DELETE":
        try:
            user.delete()
        except Exception as e:
            return str(e), 500

        return "User deleted", 204

    if request.method == "PUT":
        name = request.form.get("name")
        if not name:
            return "User name is required\n", 400

        existing_user = User.load_by_attr("name", name)
        if existing_user and existing_user.id != user.id:
            return "User name is taken\n", 400

        user.name = name
        user.save()

        return user.to_dict(), 200
