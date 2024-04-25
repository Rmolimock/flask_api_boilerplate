from flask import request
from main import app
from models.client_model import Client


def client_header():
    # check for an Authorization header
    return request.headers.get("Authorization")

def client_header_is_valid(header):
    # check for an invalid Authorization header
        return (
            isinstance(header, str)
            and len(header) > 7
            and header.startswith("Bearer ")
        )

def client_from_header(header):
    '''
    Use client authorization header token to get client object.
    Use client_header_is_valid(header) prior to calling this function.
    '''
    # extract token from Authorization header
    token = header[7:]

    # check for a valid client based on token
    return Client.load_by_attr("token", token)


@app.before_request
def before_request():
    """
    Set client and authorization token from the Authorization header, else None.
    """
 
    header = client_header()

    if not header:
        request.client = None
        request.token = None
        pass
    
    invalid_authorization = f"Invalid header. Usage: Authorization: Bearer <token>\nNot: {header}", 400
    invalid_token = "Invalid token\n", 401

    if not client_header_is_valid(header):
        return invalid_authorization
    
    client = client_from_header(header)
    if not client:
        return invalid_token

    request.client = client
    request.token = client.token