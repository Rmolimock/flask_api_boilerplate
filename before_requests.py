from main import app
from models import Client


def get_authorization_token(request):
    token = request.headers.get("Authorization")
    if not token or len(token) < 8:
        return None

    return token[7:]


def set_request_token(token):
    from flask import request

    request.token = token
    if not token:
        request.client = None

    return


def set_request_client(client):
    from flask import request

    request.client = client
    if not client:
        request.token = None

    return


@app.before_request
def before_request():
    from flask import request

    token = get_authorization_token(request)

    set_request_token(token)

    if not token:
        return

    client = Client.load_by_attr("token", token)

    set_request_client(client)
