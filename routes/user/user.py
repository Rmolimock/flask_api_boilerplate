from routes.user import users_v1

# from temp_replace.authorization import authorized_client


# add authorized_client back here once tests are rebuilt (all user routes)
@users_v1.route("/", methods=["POST"], strict_slashes=False)
def create_user():
    """
    Create a user
    """
    from flask import request
    from models import User

    name = request.form.get("name")
    handle = request.form.get("handle")
    if not (name and handle):
        return "User name and handle are required\n", 400

    data = {"name": name, "handle": handle}

    try:
        user = User(**data)
    except Exception as e:
        return str(e), 500

    if not user:
        return "Failed to create user\n", 500

    user_dict = user.to_dict()
    user.save()

    return user_dict, 201


@users_v1.route("/", methods=["GET"], strict_slashes=False)
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
        handle = request.form.get("handle")
        if not (name or handle):
            return "User name or handle is required\n", 400

        if name:
            name_taken = User.load_by_attr("name", name)
            if name_taken and name_taken.id != user.id:
                return "User name is taken\n", 400
            user.name = name

        if handle:
            handle_taken = User.load_by_attr("handle", handle)
            if handle_taken and handle_taken.id != user.id:
                return "User handle is taken\n", 400
            user.handle = handle

        user.save()

        return user.to_dict(), 200
