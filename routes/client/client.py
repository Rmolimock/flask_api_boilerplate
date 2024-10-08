from models import Client
from before_request import get_attr_from_request_form
from routes.client import clients_v1
from authorization import authorize_route


@clients_v1.route("/", methods=["GET"], strict_slashes=False)
@authorize_route
def all_clients():
    clients = Client.load_all_dict(remove_attr="token")
    return {"clients": clients}, 200


@clients_v1.route("/<id>", methods=["GET", "PUT"], strict_slashes=False)
@authorize_route
def client_by_id(id):
    from flask import request

    client = Client.load_by_id(id)

    if not client:
        return {"message": "Client not found."}, 404

    elif request.method == "GET":
        return {"client": client.to_dict()}, 200

    elif request.method == "DELETE":
        client.delete()
        return {}, 204

    # method == PUT

    name = get_attr_from_request_form(request, "name")

    if not name:
        return {"message": "Name is required"}, 400

    name_taken = Client.load_by_attr("name", name)

    if name_taken and hasattr(name_taken, "id") and name_taken.id != id:
        return {"message": "Client with this name already exists."}, 400

    client.name = name
    client.save()
    return {}, 204
