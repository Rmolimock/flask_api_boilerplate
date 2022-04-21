from pytest_bdd import scenario, given, when, then
from pytest_bdd.parsers import cfparse as parse
from tests.step_defs import CONVERTERS


@scenario('../features/run_as_is.feature', 'The database connection is established using data loaded from a config file')
def test_create_db_connection_from_config():
    pass


'''
It might be best to split this into multiple scenarios with shared steps in the future.
I might want to add tags for tests that run the application context because it takes a moment
for the app to load, and sometimes it could be enough to test if the config data is present
and complete without having to also run the app and check if it set that config data.
'''

@given(parse('a "{config_file}" exists'), target_fixture='config_file')
def existing_file(config_file):
    try:
        from config import ConfigFile
        config_file = ConfigFile(filename=config_file)
        assert config_file.data
        return config_file
    except Exception as e:
        print(e)
        assert False

@given('it has database credentials')
def has_credentials(config_file):
    try:
        credentials = config_file.database_credentials
        assert credentials
    except Exception as e:
        print(e)
        assert False


@given('they are complete')
def are_valid(config_file):
    required_credentials = ['type', 'name', 'connection', 'user', 'password']
    for credential in required_credentials:
        assert credential in config_file.database_credentials

@when('the app is running', target_fixture='app')
def app_running():
    from main import app
    assert app
    return app

@then('the app uses a database connection with those credentials')
def app_runs_locally(config_file, app):
    try:
        from db.credentials import DatabaseCredentials
        expected_uri = DatabaseCredentials.uri_from_config(config_file)
        assert app.config.get('SQLALCHEMY_DATABASE_URI') == expected_uri
    except Exception as e:
        print('--', e)
        assert False
