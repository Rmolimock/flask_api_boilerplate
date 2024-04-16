"""
POST create
GET all clients
GET, DELETE, PUT client by id
"""

from routes.client import clients_v1


@clients_v1.route("/", methods=["POST"], strict_slashes=False)
def create_client():
    """
    Create a client
    """
    from flask import request
    from models import Client

    name = request.form.get("name")
    if not name:
        return "Client name is required", 400

    try:
        client = Client(**{"name": name})
    except Exception as e:
        return str(e), 500

    if not client:
        return "Failed to create client", 500

    client_dict = client.to_dict()
    client.save()

    return client_dict, 201


@clients_v1.route("/", methods=["GET"], strict_slashes=False)
def all_clients():
    """
    Get all clients
    """
    from models import Client

    clients = Client.load_all_dict()
    if not clients:
        return "No clients found", 404

    return clients, 200


@clients_v1.route("/<id>", methods=["GET", "DELETE", "PUT"], strict_slashes=False)
def get_by_id(id):
    """
    Get, update, or delete a client by id
    """
    from flask import request
    from models import Client

    client = Client.load_by_id(id)
    if not client:
        return "Not found. Invalid client ID.", 404

    if request.method == "GET":
        return client.to_dict(), 200

    token = request.token
    if not token:
        return "Unauthorized", 401

    if token != client.token:
        return "Unauthorized", 401

    if request.method == "DELETE":
        client.delete()
        return "Client deleted", 204
    elif request.method == "PUT":
        name = request.form.get("name")
        if not name:
            return "Client name is required", 400

        existing_client = Client.load_by_attr("name", name)
        if existing_client:
            return "Client name already in use.", 400

        client.name = name
        client.save()
        return client.to_dict(), 200
