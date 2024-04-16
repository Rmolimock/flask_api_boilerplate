from main import app


@app.before_request
def before_request():
    """
    Set authorization token from the Authorization header, else None.
    """
    from flask import request

    authorization = request.headers.get("Authorization")

    if authorization:
        if not isinstance(authorization, str):
            return "Invalid Authorization header", 400
        if not len(authorization) > 7:
            return "Invalid Authorization header", 400
        if not authorization.startswith("Bearer "):
            return "Invalid Authorization header", 400

        token = authorization[7:]
        request.token = token

    else:
        request.token = None
