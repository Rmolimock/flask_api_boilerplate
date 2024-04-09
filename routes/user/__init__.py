from flask import Blueprint

users_v1 = Blueprint("users", __name__, url_prefix="/users")

from routes.user.users import *