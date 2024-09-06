from flask import Blueprint

clients_v1 = Blueprint("clients", __name__, url_prefix="/clients")

from routes.client.client import all_clients
