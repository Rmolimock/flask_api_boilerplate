from main import app
from models import Client

@app.before_request
def before_request():
    # check if request has Authorization header
    # if it does, check if the token matches a valid client
    # if it does, set the request's client and token attributes
    # if not, set them to None
    from flask import request

    token = request.headers.get("Authorization")
    if not token:
        request.client = None
        request.token = None
        return
    
    client = Client.load_by_attr("token", token)
    if not client:
        request.client = None
        request.token = None
        return
    
    request.client = client
    request.token = token