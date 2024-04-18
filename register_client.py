#!/usr/bin/env python3
"""
Register a new client with the API

Usage:
    python register_client.py <client_name>

Return: <client_token>
"""
from models.client_model import Client
from sys import argv
from main import app
from db import db

usage = "\nUsage:\n\tpython register_client.py <client_name>\n"

# check for correct usage
if not len(argv) == 2:
    print(usage)
    exit()

name = argv[1]

with app.app_context():

    # check if the client already exists
    existing_client = Client.load_by_attr("name", name)

    if existing_client:
        print("Client already exists")
    else:
        # create a new client
        client = Client(**{"name": name})
        client.save()
        print(client.token)

    db.session.remove()
    exit()
