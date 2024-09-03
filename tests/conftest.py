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

def mock_with_patch(path):
    from unittest.mock import patch
    # A.1
    patcher = patch(path)
    mock = patcher.start()
    return mock



# =============================================================================
# Helper functions for fixtures ===============================================
# =============================================================================



@pytest.fixture()
def make_request(api):
    """
    Return a function that makes requests of a given type to the test API. Optional authorization header.
    """

    def request_func(method, route, authorization_header=None, data={}):
        """
        Makes requests of a given type to the test API. Optional authorization header and PUT data.
        """
        if not isinstance(method, str):
            raise TypeError("Method must be a string")

        if method not in ["get", "post", "put", "delete", "GET", "POST", "PUT", "DELETE"]:
            raise ValueError("Invalid HTTP method specified.")
        
        method = method.lower()

        if not isinstance(route, str):
            raise TypeError("Route must be a string")

        if not isinstance(data, (dict, type(None))):
            raise TypeError("Data must be a dictionary")

        headers = {}

        if authorization_header:
            headers["Authorization"] = f"Bearer {authorization_header}"

        method_func = getattr(api, method)
        return method_func(route, headers=headers, json=data)

    return request_func



# =============================================================================
# Parameterized fixtures ======================================================
# =============================================================================



@pytest.fixture(params=["GET", "POST", "PUT-VALID", "PUT-INVALID", "DELETE"])
def method(request):
    """
    Parameterize the methods only, not routes. So GET /obj and GET /obj/{id}
    should be tested separately, not parameterized.
    """
    return request.param

@pytest.fixture()
def is_valid_data(request, method):
    return {"data": str(uuid4())} if method == "put-valid" else {}

@pytest.fixture(params=[True, False])
def is_authorized(request):
    mock_get_auth_client = mock_with_patch("authorization.get_client_from_token")
    if request.param:
        mock_get_auth_client.return_value = True
        return str(uuid4())
    else:
        mock_get_auth_client.return_value = None
        return None