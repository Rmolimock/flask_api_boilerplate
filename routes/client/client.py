from routes.client import clients_v1

@clients_v1.route("/", methods=["GET"])
def client():
    from models import Client

    return Client.load_all_dict(), 200