# Flask API Boilerplate
This is a boilerplate repo for a Flask API. I'm creating it to help me get started with new projects faster.

## Features
- [X] Automatically connect to mysql database, given user-provided credentials
- [X] A base model for serializing, deserializing, and shared methods
- [X] A client model for application clients
- [ ] A user model for identifying individual users
- [ ] A client authorization system
- [X] Automatically create tables in the database for client models
- [ ] Also for user models
- [ ] Flask-Migrate for database version control
- [ ] CRUD routes for clients and users
- [ ] Pytests for all of the above

## Requirements
- Python 3.10
- MySQL 8.0
- Flask 2.0
- Flask-Migrate 3.0
- Flask-SQLAlchemy 3.0
- PyMySQL 1.0

## Installation
1. `git clone https://github.com/Rmolimock/flask_api_boilerplate.git`
2. `cd flask_api_boilerplate`
3. `pip install -r requirements.txt`
4. Create a .env file with the following contents:
- DB_NAME=
- DB_USER=
- DB_PASSWORD=
- DB_HOST=
- DB_PORT=
- FLASK_APP=main.py
5. `FLASK_DEBUG=True flask run`
