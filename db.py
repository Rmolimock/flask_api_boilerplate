from flask_sqlalchemy import SQLAlchemy
from os import getenv


db = SQLAlchemy()

PRODUCTION = not getenv("FLASK_DEBUG")


def firebase_connection():
    import firebase_admin
    from firebase_admin import credentials
    from firebase_admin import firestore
    from os import getenv


    if PRODUCTION:
        cred = credentials.Certificate("/path/to/firebase_service_key.json")
    else:
        cred = credentials.Certificate("/path/to/firebase_service_key.json")
    firebase_admin.initialize_app(cred)
    return firestore.client()


def mysql_connection(app):
    if PRODUCTION:
        uri = "mysql+pymysql://name:password@host/database$default"
    else:
        uri = "mysql+pymysql://root:11111@localhost:3306/flask_boilerplate_db"

    app.config.update(
        SQLALCHEMY_DATABASE_URI=uri,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    db.init_app(app)
    with app.app_context():
        db.create_all()