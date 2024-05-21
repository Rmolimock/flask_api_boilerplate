# TODO:
# 1. fixture that mocks client_from_header as dummy client or None, depending upon the parameters
# 2. fixture that mocks 'client_header' in the before request to return a string like 'Authorization: Bearer {str(uuid4())}' or None for invalid token
# 3. I'm intentionally NOT mocking client_header_is_valid in case they ever change, so they will fail when appropriate

"""
parameters:
header is present, send either a token in the authorization fixture or None
    when token is valid, mock a client from client_from_header
    token is invalid, mock None
header is not present, mock client_header to return None


in before_request I want to mock client_from_header to return mock client when there IS a header and it is valid, else None
in test functions I want to have either an authorization string like 'Bearer: uuid4' or None
in test functions I want to have methods parameterized like GET all, and GET, POST, PUT, and DELETE by ID
in test functions I want to have uuid IDs for each but not for GET all


       auth string: None            valid           valid           None            
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
