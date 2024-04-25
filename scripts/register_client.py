#!/usr/bin/env python3
"""
Register a new client with the API

Usage:
    python register_client.py <client_name>

Return: <client_token>
"""
from models.client_model import Client
from db import db

def create_client(name):
    from main import app


    with app.app_context():
        existing_client = Client.load_by_attr("name", name)

        if existing_client:
            return "Client name already in use.\n"
        
        client = Client(**{"name": name})
        client.save()

        db.session.remove()

        return client.token



if __name__ == "__main__":
    from sys import argv
    
    
    # check for correct usage
    if not len(argv) == 2:
        print('\nUsage:\n\tpython register_client.py <client_name>\n')
        exit()

    name = argv[1]

    token = create_client(name)

    print(token)

