from app import create_app, register_blueprints
from db import mysql_connection
from flask_cors import CORS
from flask_migrate import Migrate

# Initialize the flask app
app = create_app()

# Enable CORS for all domains
# CHANGE THIS IN PRODUCTION
CORS(app, resources={r"/*": {"origins": "*"}})

# import all models so that they are registered with the db
from models import *

# Initialize the mysql connection
db = mysql_connection(app)

# Initialize the migration engine
migrate = Migrate(app, db)

# Register all the routes in the app
register_blueprints(app)

# Register the before and after request handlers
from before_request import before_request

# from after_requests import after_request


from authorization import authorize


@app.route("/status")
@authorize
def status():
    return {"message": "OK"}, 200
