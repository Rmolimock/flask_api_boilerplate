'''
Tests for the client API endpoints, GET all and GET, PUT, DELETE by id
'''
import pytest
from main import app


@pytest.fixture()
def test_app():
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


class TestClients:
    """
    Test the client API endpoints
    1. GET all clients
    2. GET client by id
    3. PUT client by id
    4. DELETE client by id
    - [ ] test all both with and without authorization (required by PUT and DELETE)
    - [ ] test GET, PUT, and DELETE by id with both valid and invalid client id
    """

    def test_unauthorized_get_all(self, api):
        """
        Test the GET all clients endpoint without authorization
        """
        response = api.get("/v1/clients/")
        assert response.status_code == 200
    
    def test_authorized_get_all(self, api):
        """
        Test the GET all clients endpoint with authorization
        """
        headers = {
            'Authorization': 'Bearer test_token'
        }
        response = api.get("/", headers=headers)
        assert response.status_code == 200