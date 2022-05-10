from os import getenv
from flask import jsonify


def create_app(config_filename):
    from config import ConfigFile
    from db.credentials import DatabaseCredentials
    from flask import Flask
    from flask_migrate import Migrate
    from flask_sqlalchemy import SQLAlchemy


    app = Flask(__name__)
    config_file = ConfigFile(filename=config_filename)
    uri = DatabaseCredentials.uri_from_config(config_file=config_file)
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)
    return app


IN_PRODUCTION = getenv('IN_PRODUCTION')
CONFIG_FILENAME = 'config.ini'

app = create_app(CONFIG_FILENAME)

@app.route('/status', methods=['GET'], strict_slashes=False)
def status():
    return jsonify({
        'status': 'OK'
        }), 200

# handle errors (abort)
@app.errorhandler(400)
def bad_request(error) -> str:
    return jsonify({"error": "bad Request, https required"}), 400


@app.errorhandler(404)
def not_found(error) -> str:
    return jsonify({"error": "not found"}), 404

@app.errorhandler(403)
def Forbidden(error) -> str:
    return jsonify({"error": "forbidden"}), 403

@app.errorhandler(401)
def Unauthorized(error) -> str:
    return jsonify({"error": "unauthorized"}), 401


if __name__ == '__main__':
    pass
