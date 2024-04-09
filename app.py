def create_app():
    from flask import Flask
    from flask_cors import CORS

    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    return app


def register_blueprints(app):
    from routes import API_VERSIONS

    for v in API_VERSIONS:
        app.register_blueprint(v)