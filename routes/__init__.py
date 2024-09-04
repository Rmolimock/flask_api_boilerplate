from flask import Blueprint


from routes.client import clients_v1

v1 = Blueprint("v1", __name__, url_prefix="/v1")

blueprints = [clients_v1]

for bp in blueprints:
    v1.register_blueprint(bp)

API_VERSIONS = [v1]