from setup import ENVS, orm_factory, app_factory
from endpoints import some_endpoint


app, db, migrate = app_factory()

app.register_blueprint(some_endpoint)

# must import models for flask_migrate to track changes
from models import *

@app.route('/')
def index():
    return 'Home page'


if __name__ == '__main__':
     app.run(host='127.0.0.1', port=5000, debug=True)