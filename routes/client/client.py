from models import Client
from routes.client import clients_v1


@clients_v1.route('/', methods=['GET'], strict_slashes=False)
def all_clients():
    clients = Client.load_all()
    return {"clients": clients}, 200