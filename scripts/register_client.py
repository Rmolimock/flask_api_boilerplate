#!/usr/bin/env python3
"""
Register a new client with the API

Usage:
    python register_client.py <client_name>

Return: <client_token>
"""
from main import app
from db import db
from models.client_model import Client


def create_client(name):


    with app.app_context():
        existing_client = Client.load_by_attr("name", name)

        if existing_client:
            db.session.remove()
            return "Client name already in use.\n"
        
        client = Client(**{"name": name})
        client.save()


        return client.token



if __name__ == "__main__":
    from sys import argv
    
    
    # check for correct usage
    if not len(argv) == 2:
        print('\nError. Correct usage:\n\tpython register_client.py <client_name>\n')
        exit()

    name = argv[1]

    token = create_client(name)

    print(token)
