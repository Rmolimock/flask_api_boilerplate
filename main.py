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


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name


db.create_all()

admin = User(id=2, name='admin@example.com')
db.session.add(admin)
db.session.commit()

a = User.query.all()