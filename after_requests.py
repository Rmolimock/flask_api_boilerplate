from main import app


@app.after_request
def after_request(response):
    # close the db session after each request to avoid memory leaks
    from db import db

    db.session.remove()
    return response
