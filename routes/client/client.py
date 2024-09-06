from models import Client
from before_request import get_request_form_attr
from routes.client import clients_v1
from authorization import authorize


@clients_v1.route("/", methods=["GET"], strict_slashes=False)
@authorize
def all_clients():
    clients = Client.load_all()
    return {"clients": clients}, 200


@clients_v1.route("/<id>", methods=["GET", "PUT"], strict_slashes=False)
@authorize
def client_by_id(id):
    from flask import request

    client = Client.load_by_id(id)
    if not client:
        return {"message": "Client not found."}, 404
    
    if request.method == "PUT":
        name = get_request_form_attr(request, "name")
        if not name:
            print(1)
            return {"message": "Name is required"}, 400
        
        name_taken = Client.load_by_attr("name", name)
        if name_taken and hasattr(name_taken, 'id') and name_taken.id != id:
            print(2)
            return {"message": "Client with this name already exists."}, 400
        
        client.name = name
        client.save()
        return {}, 204

    return {"client": client.to_dict()}, 200
