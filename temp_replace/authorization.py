"""
Authorize requests belong to a valid client.
"""

from functools import wraps

# replace with error handling for unauthorized requests
unauthorized_message = "\nUnauthorized. Client token required.", 401


def authorized_client(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        from flask import request

        if not request.client:
            return unauthorized_message
        return func(*args, **kwargs)

    return wrapper
