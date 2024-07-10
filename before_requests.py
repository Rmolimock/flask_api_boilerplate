from main import app


@app.before_request
def before_request():
    # check if request has Authorization header
    # if it does, check if the token matches a valid client
    # if it does, set the request's client and token attributes
    # if not, set them to None
    