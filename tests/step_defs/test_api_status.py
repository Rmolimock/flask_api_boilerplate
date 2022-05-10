from pytest_bdd import scenario, given, when, then
from pytest_bdd.parsers import cfparse as parse
from tests.step_defs import CONVERTERS
import pytest


@pytest.fixture(scope='module')
def fixture1():
   return "Yes"


@scenario('../features/run_as_is.feature', 'The API has a status endpoint for verifying that it is operational')
def test_api_status():
    pass


@given('the API is running', target_fixture='app')
def api_running(app_setup):
    assert app_setup


@when('a get request is sent to /status', target_fixture='response')
def get_status(app_setup):
    with app_setup.test_client() as client:
        response = client.get('/status')
        assert response
        return response

@then('a status code of 200 is returned')
def status_is_200(response):
    status = response.status_code
    assert status == 200

