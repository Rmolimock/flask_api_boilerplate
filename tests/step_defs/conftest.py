import pytest


@pytest.fixture(scope='module')
def app_setup():
    from main import app
    return app
