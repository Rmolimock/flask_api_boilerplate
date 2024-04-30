# Flask API Boilerplate
This is a boilerplate repo for a Flask API. I'm creating it to help me get started with new projects faster.

## Features
- [X] Automatically connect to mysql database, given user-provided credentials
- [X] A base model for serializing, deserializing, and shared methods
- [X] A client model for application clients
- [X] A user model for identifying individual users
- [X] Automatically create tables in the database for client models
- [X] Flask-Migrate for database version control
- [X] CRUD routes for clients and users
- [ ] Pytests for all of the above

## Requirements
- Python 3.10
- MySQL 8.0
- Flask 2.0
- Flask-Migrate 3.0
- Flask-SQLAlchemy 3.0
- PyMySQL 1.0

## Installation
1. git clone https://github.com/Rmolimock/flask_api_boilerplate.git
2. cd flask_api_boilerplate
3. pip install -r requirements.txt
4. Create a .env file with the following contents:
- DB_NAME=
- DB_USER=
- DB_PASSWORD=
- DB_HOST=
- DB_PORT=
- FLASK_APP=main.py
- PYTHONPATH='.'
5. sudo apt-get install inotify-tools # for running run_pytest_on_save.sh
6. chmod +x run_pytest_on_save.sh
7. sudo apt install zenity # for running run_pytest_on_save.sh
8. ./run_pytest_on_save.sh # in a separate terminal
9. flask db init # if you don't have migrations folder, alembic.ini, or env.py yet
10. flask db migrate
11. flask db upgrade
12. sudo apt-get install mysql-server # if you don't have MySQL installed
13. mysql -u root -p # log in to MySQL in another terminal
14. FLASK_DEBUG=True flask run
