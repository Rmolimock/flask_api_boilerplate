
def env_variables(envs) -> dict:
    '''
    Load a list of environment variables into memory.
    '''
    from os import getenv
        
    loaded_envs = {}
    for value in envs:
        loaded_envs[value] = getenv(value)
        if not loaded_envs[value] and not value == 'FLASK_ENV':
            raise KeyError(f'{value} env variable was not found upon startup')
    return loaded_envs


# use these globally?
envs = [
        'DB_TYPE', 'DB_USER', 'DB_PAS', 'DB_NAME',
        'DB_CON', 'FLASK_APP', 'FLASK_ENV'
    ]
ENVS = env_variables(envs)


def orm_factory(app, config: dict) -> tuple:
    '''
    Configure flask app with a given orm.
    '''
    from flask_sqlalchemy import SQLAlchemy

    # edge cases
    if not app:
        raise ValueError('orm factory is missing the application context')
    if not config or not config.get('orm'):
        raise KeyError('orm factory needs to know which orm to use')
    orm = config.get('orm')
    accepted_orms = ['flask_sqlalchemy']
    if not orm in accepted_orms:
        raise ValueError(f'orm factory recieved an invalid value for orm: {config.get("orm")}')
    database_connection_uri = config.get('database_connection_uri')
    if not database_connection_uri:
        raise KeyError('orm factory is missing a database_connection_uri')

    # configurations
    if config.get('orm') == 'flask_sqlalchemy':
        from db import database_factory
        app.config['SQLALCHEMY_DATABASE_URI'] = database_connection_uri
        db = database_factory(app, 'flask_sqlalchemy')
        return (app, db)


def app_factory(config=None) -> tuple:
    '''
    Initialize a flask application with config data.
    If no data is passed, defaults values are used.
    '''
    from flask import Flask
    from flask_migrate import Migrate

    # edge cases
    if not config:
        # default settings
        db_type = ENVS.get('DB_TYPE')
        db_user = ENVS.get('DB_USER')
        db_pas = ENVS.get('DB_PAS')
        db_name = ENVS.get('DB_NAME')
        config = {
            'orm': 'flask_sqlalchemy',
            'database_connection_uri': f"{db_type}://{db_user}:{db_pas}@localhost:3306/{db_name}"
        }

    # configuration
    flask_app = Flask(__name__)
    app, db = orm_factory(flask_app, config)
    migrate = Migrate(app, db)

    # other config options to be set here

    return app, db, migrate