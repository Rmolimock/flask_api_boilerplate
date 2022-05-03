# Flask API Boilerplate
This repo is intended to become a reusable starting point for the creation of new API services. Eventually, creating a basic REST service should be as simple as adding database credentials to a config file, describing the model(s) in json, and running the app. This project is being developed with TDD/BDD using pytest-bdd. Ideally (though not quite in actuality), all code should be developed to satisfy the description of high-level behavior.

## Installation
```sh
git clone https://github.com/Rmolimock/flask_api_boilerplate.git
# add your database credentials to config.ini under [DATABASE_CREDENTIALS]
# add your objects to a json file (tbt) for creation of tables and REST endpoints
. ./setup 
update_endpoints=1 flask run
```
The setup file sets the appropriate environment variables for flask, such as:
| Environment Variable | Value |
| ------ | ------ |
| PYTHONPATH | '.' |
| FLASK_APP | main |
| FLASK_ENV | development or production |
1. FLASK_ENV is set to production only if the local environment contains IN_PRODUCTION, set to anything that evaluates true. This should be included in an app.yaml file so it's only true in the hosted environment.
2. update_endpoints tells the app you have provided new json data about the objects for which you want REST endpoints. This should only be true the first time you run the api. It will produce classes with the attributes shown in the json, tables in the database, fill those tables with values (if any) in the json, and create basic GET, PUT, POST, and DELETE endpoints for those objects.


## Usage (after first time)
```sh
flask run
```

## Features
1. Connect to a database using user-provided credentials ✓
2. Establish Object Relational Mapping with SQLAlchemy ✓
3. Establish database version control and backpopulation with FlaskMigrate
4. Create classes for objects based on user-provided json data
5. Create tables for those objects in the database if they don't already exist
6. Insert values from that json data into the database
7. Create basic GET, POST, PUT, and DELETE endpoints for each of those objects.
8. Contain all boilerplate functionality in a v.0 Blueprint, and make it easy for the user to turn their modifications into a v.1.
9. dynamically select which database to use (QA/staging/production) based on request data
10. authenticate requesting service
11. authorize requesting service



© Russell Molimock - 2022
