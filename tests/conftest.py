# TODO:
# 1. fixture that mocks client_from_header in the before request as a dummy client or None, depending upon the parameters (when athorization parmeter is the valid one)
# 2. fixture that goes to the tests for an authorization header that returns a string like 'Bearer {str(uuid4())}' or None for (when authorization parameter is the valid one)
# 3. I'm intentionally NOT mocking client_header_is_valid in case they ever change, so they will fail when appropriate from getting either the 'Bearer...' or not
# 4. I would also like to parameterize the methods and dummy ids for all methods except GET / (GET all), but I'm not sure how to do that yet

"""
parameters:
header is present, send either a token in the authorization fixture or None
    assume the token is valid, mock a client from client_from_header
header is not present, mock client_header to return None


in before_request I want to mock client_from_header to return mock client when there IS a header and it is valid, else None
in test functions I want to have either an authorization string like 'Bearer: uuid4' or None
in test functions I want to have methods parameterized like GET all, and GET, POST, PUT, and DELETE by ID
in test functions I want to have uuid IDs for each but not for GET all


client_from_header: None            mock client     mock_client     None
            method: GET all 200     GET all 200     GET by ID 200   GET by ID 401
                ID: None            None            str(uuid4())    str again
            

"""

import pytest
from uuid import uuid4


@pytest.fixture()
def test_app():
    from main import app

    # configure the app for testing
    # SETUP
    app.config["TESTING"] = True

    # CLEAN UP
    yield app


@pytest.fixture()
def api(test_app):
    # initiate the test client, which I'll refer to as api
    # to avoid confusion with client objects
    return test_app.test_client()


@pytest.fixture(params=[True, False])
def authorization(request):
    if request.param:
        yield f"Bearer: {str(uuid4())}"
    else:
        yield None

@pytest.fixture(params=['GET', 'POST', 'PUT', 'DELETE'])
def method(request):
    return request.param.lower()

@pytest.fixture(params=[None, str(uuid4())])
def id(request):
    return request.param




# but then these parameters all need to influence which functions get mocked and how
# I'm not sure how to do that. Maybe a parent fixture w/ parameters that calls the others?
# like a scenarios fixture which has a dict of all the combos and then pass that into the authorization, id, and method fixtures