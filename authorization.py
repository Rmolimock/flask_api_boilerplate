from models import Client
from flask import request
from functools import wraps


unauthorized_message = {"message": "Unauthorized\n"}, 401


def get_authorization_token(request):
    """
    Extracts the authorization token from the request headers, if present.
    """
    token = request.headers.get("Authorization")
    if not token or len(token) < 8:
        return None

    return token[7:]


def get_client_from_token(token):
    """
    Returns client based on given token if valid, else None.
    This extra function wrapping around load_by_attr is needed for mocking in tests."""
    client = Client.load_by_attr("token", token)
    return client


# wrapper to check for authorization token in request
def authorize(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = get_authorization_token(request)
        client = get_client_from_token(token)
        if not client:
            return unauthorized_message

        return func(*args, **kwargs)

    return wrapper
