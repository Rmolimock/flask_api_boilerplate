"""
Before request functions for Flask app.
Handles client authorization.
"""

from main import app
from models.client_model import Client


def client_header(request):
    """
    Retrieve the Authorization header from the flask request
    Return: Authorization header string if it exists, else None.
    """

    return request.headers.get("Authorization")


def client_header_is_valid(header):
    '''
    Check if the Authorization header is valid.
    Return: True if valid, else False.
    '''

    return isinstance(header, str) and len(header) > 7 and header.startswith("Bearer ")


def client_from_header(header):
    """
    Extract the client token from the header.
    Return: Client object if token is valid, else None.
    """

    # this check is redundant in the context of the before_request function
    # but necessary if ever used in a different context
    if not client_header_is_valid(header):
        return None

    # extract token from Authorization header
    token = header[7:]

    # check for a valid client based on token
    return Client.load_by_attr("token", token)


@app.before_request
def before_request():
    """
    Set client and authorization token from the Authorization header if present and valid, else None.
    Return: N/A
    """
    from flask import request

    header = client_header(request)

    # for routes that do not require authorization
    if not header:
        request.client = None
        request.token = None
        return

    """
    # These should be flask error handlers so I can use them consistently in the routes
    # I'll leave it to the authorization wrapper to return the error message
    invalid_authorization = f"Invalid header. Usage: Authorization: Bearer <token>\nNot: {header}", 400
    invalid_token = "Invalid token\n", 401
    
    # header exists but is invalid, return error so client can correct
    if not client_header_is_valid(header):
        return invalid_authorization
    """
    # valid header but no client, return error for security
    client = client_from_header(header)
    # if not client:
    #    return invalid_token
    # in the future generate a warning that does not affect the response somehow

    request.client = client
    if client:
        request.token = client.token
    else:
        request.token = None
