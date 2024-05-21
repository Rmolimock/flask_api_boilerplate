"""
Tests for the client API endpoints, GET all and GET, PUT, DELETE by id
"""

import pytest
from main import app
from uuid import uuid4


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


@pytest.fixture()
def mock_token():
    return str(uuid4())


scenarios = [
    {"header_present": True, "token_valid": True, "mock_return": "mock_client"},
    {"header_present": True, "token_valid": False, "mock_return": None},
    {"header_present": False, "token_valid": None, "mock_return": None},
]


@pytest.fixture(params=scenarios)
def setup_authorization(request, mock_client_before_request, mock_client, mock_token):
    scenario = request.param

    if scenario["header_present"]:
        if scenario["token_valid"]:
            mock_client_before_request.load_by_attr.return_value = mock_client
        else:
            mock_client_before_request.load_by_attr.return_value = None

    # Return the headers based on whether the header should be present
    headers = (
        {"Authorization": f"Bearer {mock_token}"} if scenario["header_present"] else {}
    )
    return headers, mock_client_before_request


@pytest.fixture()
def make_request(api):
    """
    Return a function that can make requests to the API. Optionally includes an authorization header.
    """

    def request(method, route, token=None, data=None):
        if method not in ["get", "post", "put", "delete"]:
            raise ValueError("Invalid HTTP method specified.")

        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        method_func = getattr(api, method)
        return method_func(route, headers=headers, json=data)

    return request


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


'''
    def test_authorized_put_by_id(self, api, mock_client, mock_client_before_request):
        """
        Test the PUT client by id endpoint with authorization
        """
        # MOCK VALUES
        mock_id = str(uuid4())
        mock_token = str(uuid4())
        headers = {'Authorization': f'Bearer {mock_token}'}
        json = {'name': 'test_name'}

        mock_client.load_by_id.return_value = mock_client
        # before_request checks for valid client by authorization token
        # must be client object because it then checks client.token
        mock_client_before_request.load_by_attr.return_value = mock_client
        # route checks if the proposed client name is already in use
        mock_client.load_by_attr.return_value = False

        # ACTIONS
        response = api.put(f'/v1/clients/{mock_id}', headers=headers, data=json)
        print(response.data)

        # ASSERTIONS
        assert response.status_code == 200
        mock_client.load_by_id.assert_called_once_with(mock_id)
        mock_client_before_request.load_by_attr.assert_called_once_with(
            'token', mock_token
        )


    def test_put_by_id(self, api, setup_authorization, mock_token):
        headers, mock_client_before_request = setup_authorization

        # MOCK VALUES
        mock_id = str(uuid4())
        json = {"name": "test_name"}



To Test:
1. header present | not
2. when present, is token valid | not
3. only test token valid/invalid when header is present
Plan:
parameterize the fixtures themselves. So there will be a fixture for each of the following:
headers: which will have True/False parameters, and will return a dict with or without the Authorization key
then in the tests I can just assign the headers to the request function, regardless of their value
token: also will have True/False but only when headers are present.
So create a dict of scenarios and pass that into a parameterized authorization fixture
fixture must return tuple of headers and mock_client_before_request
'''
