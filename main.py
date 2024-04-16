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
mysql_connection(app)

# Register all the routes in the app
register_blueprints(app)

# Register the before and after request handlers
from before_requests import before_request
from after_requests import after_request


@app.route("/", methods=["GET"], strict_slashes=False)
def status():
    print("in the request")
    return "OK", 200
