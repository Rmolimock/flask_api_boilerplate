from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import ConfigFile
from db.credentials import DatabaseCredentials



CONFIG_FILENAME = 'config.ini'


config_file = ConfigFile(filename=CONFIG_FILENAME)
        

app = Flask(__name__)
# in app factory, set other app.config data from config_file
uri = DatabaseCredentials.uri_from_config(config_file=config_file)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


