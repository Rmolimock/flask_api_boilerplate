from crypt import methods
import json
from urllib import request
from endpoints import some_endpoint
from flask import request, jsonify

@some_endpoint.route('/', methods=['GET', 'POST'], strict_slashes=None)
def get_all():
    
    if request.method == 'GET':
        # get objects from database -
        # actual db sessions not created yet
        return jsonify({
            'status': 'OK',
            'objects': {
                'one': 'one',
                'two': 'two',
                'three': 'three'
            }
        }), 200
    elif request.method == 'POST':
        # create object and save to the database
        # actual db sessions not created yet
        return jsonify({
            'status': 'OK',
            'message': 'object created'
        }), 200
