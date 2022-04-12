from flask import Blueprint

some_endpoint = Blueprint('endpoint_name', __name__, url_prefix="/endpoint_prefix")

from endpoints.endpoint_template import *