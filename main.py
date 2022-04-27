from config import ConfigFile
from db.credentials import DatabaseCredentials
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from os import getenv


IN_PRODUCTION = getenv('IN_PRODUCTION')
CONFIG_FILENAME = 'config.ini'

config_file = ConfigFile(filename=CONFIG_FILENAME)
        

app = Flask(__name__)
# in app factory, set other app.config data from config_file
uri = DatabaseCredentials.uri_from_config(config_file=config_file)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route('/')
def index():
    return 'index'

@app.route('/test')
def tes():
    from models import BoilerplateModel
    from flask import jsonify
    with app.app_context():
        try:
            m = BoilerplateModel.query.filter_by(boiler='test_boiler').first()
            if m:
                return jsonify(m.to_dict())
            else:
                return {}
        except Exception as e:
            return str(e)


if __name__ == '__main__':
    pass