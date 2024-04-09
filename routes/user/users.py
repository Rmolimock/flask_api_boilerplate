from routes.user import users_v1

@users_v1.route("", methods=["POST"])
def one():
    return "User created!"