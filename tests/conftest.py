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

def load_mock_obj_by_attr(mock_class, attr_name, value):
    from unittest.mock import MagicMock

    # 1. create and set up the mock instance
    mock_obj = MagicMock()
    # set mock object attribute of name attr_name with value
    setattr(mock_obj, attr_name, value)
    mock_obj.to_dict = MagicMock(return_value={attr_name: value})
    # 2. the mock class to returns the mock instance with load_by_attr
    mock_class.load_by_attr.return_value = mock_obj
    return mock_obj

def mock_obj_if_valid_id(is_valid_id, mock_class):
    if is_valid_id:
        return load_mock_obj_by_id(mock_class, is_valid_id)
    else:
        mock_class.load_by_id.return_value = None
        mock_class.load_by_attr.return_value = None
        return None


def mock_obj_if_authorized(is_authorized, mock_class):
    if is_authorized:
        mock_obj = load_mock_obj_by_attr(mock_class, "token", is_authorized)
        return mock_obj
    else:
        mock_class.load_by_id.return_value = None
        mock_class.load_by_attr.return_value = None
        return None

def mock_with_patch(path):
    from unittest.mock import patch
    # A.1
    patcher = patch(path)
    mock = patcher.start()
    return mock

@pytest.fixture()
def make_request(api):
    """
    Return a function that can make requests to the API. Optionally includes an authorization header.
    """

    def request_func(method, route, is_authorized=None, data={}):
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


@pytest.fixture(params=["get", "put-valid", "put-invalid", "delete"])
def method_no_post_put_data(request):
    """
    Parameterize the methods only, not routes. So GET /obj and GET /obj/{id}
    should be tested separately, not parameterized. Check both valid/invalid PUT data.
    """
    return request.param


@pytest.fixture(params=[True, False])
def is_valid_id(request):
    return str(uuid4()) if request.param else None


@pytest.fixture(params=[True, False])
def is_authorized(request):
    return str(uuid4()) if request.param else None

@pytest.fixture()
def is_valid_data(request, method_no_post_put_data):
    return {"name": str(uuid4())} if method_no_post_put_data == "put-valid" else {}
