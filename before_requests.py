from main import app


@app.before_request
def before_request():
    # Authorization logic goes here
    print('in the before')
    pass