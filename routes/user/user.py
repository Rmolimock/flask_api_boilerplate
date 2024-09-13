from models import User
from routes.user import users_v1


@users_v1.route("/", methods=["GET"], strict_slashes=False)
def all_users():
    users = User.load_all_dict(remove_attr="client_id")
    return {"users": users}, 200