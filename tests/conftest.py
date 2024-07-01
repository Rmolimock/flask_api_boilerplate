# if authorization header is present and valid in a request
# then flask's request object will have a token attribute
# and the models.Client.load_by_attr("token", token) method
# will return a mock client object with the token attribute
# and the id matching the mocked client id

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

pytest.fixture()
def mock_id():
    return str(uuid4())

@pytest.fixture()
def make_request(api):
    """
    Return a function that can make requests to the API. Optionally includes an authorization header.
    """

    def request(method, route, token=None, data=None):
        if not isinstance(method, str):
            raise TypeError("Method must be a string")
        
        if method not in ["get", "post", "put", "delete"]:
            raise ValueError("Invalid HTTP method specified.")
        
        if not isinstance(route, str):
            raise TypeError("Route must be a string")
        
        if not isinstance(token, (str, type(None))):
            raise TypeError("Token must be a string or None")

        if not isinstance(data, (dict, type(None))):
            raise TypeError("Data must be a dictionary")

        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        method_func = getattr(api, method)
        return method_func(route, headers=headers, json=data)

    return request


@pytest.fixture(params=[True, False])
def has_valid_id(request, mocker):
    def is_valid_id(mock_class_path):
        if request.param:
            obj_id = str(uuid4())
            mock_class = mocker.patch(mock_class_path)
            mock_obj = mocker.MagicMock()
            mock_obj.id = obj_id
            mock_class.load_by_id.return_value = mock_obj
            return obj_id
        else:
            return None
            
    return is_valid_id

