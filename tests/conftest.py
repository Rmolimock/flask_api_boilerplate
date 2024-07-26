# if authorization header is present and valid in a request
# then flask's request object will have a token attribute
# and the models.Client.load_by_attr("token", token) method
# will return a mock client object with the token attribute
# and the id matching the mocked client id

import pytest
from uuid import uuid4


# =============================================================================
# Basics, App and API =========================================================
# =============================================================================


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


# =============================================================================
# Simple mock values for fixtures =============================================
# =============================================================================


pytest.fixture()


def mock_id():
    return str(uuid4())


# =============================================================================
# Helper functions for fixtures ===============================================
# =============================================================================


def load_mock_obj_by_id(mock_class, id):
    from unittest.mock import MagicMock

    # 1. create and set up the mock instance
    mock_obj = MagicMock()
    mock_obj.id = id
    mock_obj.to_dict = MagicMock(return_value={"id": id})

    # 2. the mock class to returns the mock instance with load_by_id
    mock_class.load_by_id.return_value = mock_obj
    return mock_obj

@pytest.fixture()
def mock_obj_if_valid_id(is_valid_id):
    def func(mock_class):
        if is_valid_id:
            return load_mock_obj_by_id(mock_class, is_valid_id)
        else:
            return None

    return func

@pytest.fixture()
def mock_obj_if_authorized(mocker, is_authorized):
    def func(mock_class):
        if is_authorized:
            # mock object instance, make class return it by .token, make instance.to_dict return dict of attrs
            mock_obj = mocker.MagicMock()
            mock_obj.token = is_authorized
            mock_class.load_by_attr.return_value = mock_obj
            mock_obj.to_dict = mocker.MagicMock(return_value={"token": is_authorized})
            print(mock_obj.token, 'in conftest')
            return mock_obj
        else:
            return None

    return func

@pytest.fixture()
def make_request(api):
    """
    Return a function that can make requests to the API. Optionally includes an authorization header.
    """

    def request_func(method, route, is_authorized=None, data=None):
        """
        Simulate making a request to the API with the Authorization header present only when token is present.
        """
        if not isinstance(method, str):
            raise TypeError("Method must be a string")

        if method not in ["get", "post", "put", "delete"]:
            raise ValueError("Invalid HTTP method specified.")

        if not isinstance(route, str):
            raise TypeError("Route must be a string")

        if not isinstance(data, (dict, type(None))):
            raise TypeError("Data must be a dictionary")

        headers = {}
        """if authorized:
            # will I need access to the token in the test function?
            # I'll need it here to mock a response, and I'll want it in the test
            # function so I can assert that the client was loaded with the correct token
            headers["Authorization"] = f"Bearer {authorization_token}"
            before_client_class = get_mock_class("before_requests.Client")
            attrs = {
                'token': authorization_token,
            }
            mock_client = get_mock_object(before_client_class, **attrs)
        """
        if is_authorized:
            headers["Authorization"] = f"Bearer {is_authorized}"

        method_func = getattr(api, method)
        return method_func(route, headers=headers, json=data)

    return request_func


# =============================================================================
# Parameterized fixtures ======================================================
# =============================================================================


@pytest.fixture(params=["get", "post", "put", "delete"])
def method(request):
    """
    Parameterize the methods only, not routes. So GET /obj and GET /obj/{id}
    should be tested separately, not parameterized.
    """
    return request.param


@pytest.fixture(params=["get", "put", "delete"])
def method_no_post(request):
    """
    Parameterize the methods only, not routes. So GET /obj and GET /obj/{id}
    should be tested separately, not parameterized.
    """
    return request.param


@pytest.fixture(params=[True, False])
def is_valid_id(request):
    return str(uuid4()) if request.param else None

@pytest.fixture(params=[True, False])
def is_authorized(request):
    return str(uuid4()) if request.param else None

