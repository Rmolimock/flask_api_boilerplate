"""
from flask import Blueprint

clients_v1 = Blueprint("clients", __name__, url_prefix="/clients")

from routes.client.client import all_clients, get_by_id, create_client
"""

from flask import Blueprint

users_v1 = Blueprint("users", __name__, url_prefix="/users")

from routes.user.user import *
