from models import Client


def get_request_token(request):
    """
    Get the token from the request, if it exists. For testing purposes.
    """
    return request.token if hasattr(request, "token") else None


def get_request_form_attr(request, attr):
    """
    Get the attribute from the request. For testing purposes.
    """
    return request.form.get(attr)


unauthorized_message = "Unauthorized\n", 401


# Authorization wrapper function:
# import functools wrapper
from functools import wraps

# decorator function
def authorized(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        from flask import request

        request = get_request_token(request)
        token = get_request_token(request)

        if not token:
            return unauthorized_message

        client = Client.load_by_attr("token", token)
        if not client:
            return unauthorized_message

        return f(*args, **kwargs)

    return decorated