"""
Tests for the client API endpoints, GET all and GET, PUT, DELETE by id
"""

import pytest
from main import app
from uuid import uuid4


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


@pytest.fixture()
def mock_client(mocker):
    # Initialize a shared mock client for TestClients tests
    mock_client = mocker.patch("routes.client.client.Client")
    return mock_client


@pytest.fixture()
def mock_client_before_request(mocker):
    # Initialize a shared mock client for TestClients tests
    mock_client = mocker.patch("before_requests.Client")
    return mock_client


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
        # MOCK VALUES (none)
        # ACTIONS
        response = api.get("/v1/clients/")

        # ASSERTIONS
        assert response.status_code == 200

    def test_authorized_get_all(self, api, mock_client_before_request):
        """
        Test the GET all clients endpoint with authorization
        """
        # MOCK VALUES
        mock_token = str(uuid4())
        headers = {"Authorization": f"Bearer {mock_token}"}

        # ACTIONS
        response = api.get("/", headers=headers)

        # ASSERTIONS
        assert response.status_code == 200
        mock_client_before_request.load_by_attr.assert_called_once_with(
            "token", mock_token
        )

    def test_unauthorized_get_by_id(self, api, mock_client):
        """
        Test the GET client by id endpoint without authorization
        """
        # MOCK VALUES
        mock_id = str(uuid4())
        mock_client.load_by_id.return_value = mock_client

        # ACTIONS
        response = api.get(f"/v1/clients/{mock_id}")

        # ASSERTIONS
        assert response.status_code == 200
        mock_client.load_by_id.assert_called_once_with(mock_id)

    def test_authorized_get_by_id(self, api, mock_client, mock_client_before_request):
        """
        Test the GET client by id endpoint with authorization
        """
        # MOCK VALUES
        mock_id = str(uuid4())
        # Bool would cause error, and must be mocked to avoid genuinely loading a client
        mock_client.load_by_id.return_value = mock_client
        mock_token = str(uuid4())
        headers = {"Authorization": f"Bearer {mock_token}"}

        # ACTIONS
        response = api.get(f"/v1/clients/{mock_id}", headers=headers)

        # ASSERTIONS
        assert response.status_code == 200
        mock_client.load_by_id.assert_called_once_with(mock_id)
        mock_client_before_request.load_by_attr.assert_called_once_with(
            "token", mock_token
        )

    def test_unauthorized_put_by_id(self, api, mock_client, mock_client_before_request):
        """
        Test the PUT client by id endpoint without authorization
        """
        # MOCK VALUES
        mock_id = str(uuid4())

        # ACTIONS
        response = api.put(f"/v1/clients/{mock_id}")

        # ASSERTIONS
        assert response.status_code == 401
        mock_client_before_request.load_by_id.assert_not_called()

    """
    def test_authorized_put_by_id(self, api, mock_client, mock_client_before_request):
        Test the PUT client by id endpoint with authorization
        # MOCK VALUES
        mock_id = str(uuid4())
        mock_token = str(uuid4())
        headers = {
            'Authorization': f'Bearer {mock_token}'
        }
        mock_client_before_request.load_by_attr.return_value = mock_client
        mock_client.token = mock_token

        # ACTIONS
        response = api.put(f'/v1/clients/{mock_id}', headers=headers)

        # ASSERTIONS
        assert response.status_code == 200
        mock_client_before_request.load_by_id.assert_not_called()
    """
