def create_app():
    from flask import Flask

    app = Flask(__name__)
    return app


def register_blueprints(app):
    from routes import API_VERSIONS

    for v in API_VERSIONS:
        app.register_blueprint(v)
