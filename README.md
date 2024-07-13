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
- [ ] Pytests for clients
- [ ] Pytests for users
- [ ] Pytests for shared methods
- [ ] Make pytests scalable with TestBase


## Requirements
- Python 3.10
- MySQL 8.0
- Flask 2.0
- Flask-Migrate 3.0
- Flask-SQLAlchemy 3.0
- PyMySQL 1.0
- Inotify-tools

## Installation
### Clone the repo, install requirements, and create a .env file
1. git clone https://github.com/Rmolimock/flask_api_boilerplate.git
2. cd flask_api_boilerplate
3. pip install -r requirements.txt
4. Create a .env file with the following contents (to be added to mysql db once installed in step 9):
- DB_NAME=
- DB_USER=
- DB_PASSWORD=
- DB_HOST=
- DB_PORT=
- FLASK_APP=main.py
- PYTHONPATH='.'
### Optionally setup a test error alert window
5. sudo apt-get install inotify-tools # for running run_pytest_on_save.sh
6. sudo apt install zenity # for running run_pytest_on_save.sh
7. chmod +x run_pytest_on_save.sh
8. ./run_pytest_on_save.sh # in a separate terminal

### Install MySQL
9. sudo apt-get install mysql-server # if you don't have MySQL installed
10. mysql -u root -p 
11. sudo mysql # to enter into the mysql shell, then within the shell:
12. ALTER USER 'user_from_.env_file-probably_root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password_from_.env_file';
FLUSH PRIVILEGES;
CREATE DATABASE 'database_name_from_.env_file';
EXIT;
### Setup database version control
13. flask db init # if you don't have migrations folder, alembic.ini, or env.py yet
14. flask db migrate
15. flask db upgrade
### Run the app
16. FLASK_DEBUG=True flask run





# temp to do list
- [ ] delete authorization, before_request, and test files
- [ ] create tests for authorization (which includes before_request functionality) prior to recreating it
- [ ] allow tests to inform the structure of the flow of authorization
- [ ] then parameterize the tests for different scenarios