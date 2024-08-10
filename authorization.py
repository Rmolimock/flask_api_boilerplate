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