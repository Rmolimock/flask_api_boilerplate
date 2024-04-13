from app import create_app, register_blueprints
from db import mysql_connection
from flask_cors import CORS

# Initialize the flask app
app = create_app()

# Enable CORS for all domains
# CHANGE THIS IN PRODUCTION
CORS(app, resources={r"/*": {"origins": "*"}}) 

# import all models so that they are registered with the db
from models import *

# Initialize the mysql connection
#mysql_connection(app) waiting for db to be ready in production

# Register all the routes in the app
register_blueprints(app)

@app.before_request
def before_request():
    # Authorization logic goes here
    pass

@app.after_request
def after_request(response):
    # close the db session after each request to avoid memory leaks
    from db import db
    db.session.remove()
    return response

@app.route('/')
def status():
    return 'OK', 200
