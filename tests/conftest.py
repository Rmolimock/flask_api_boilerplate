import pytest
from uuid import uuid4


# =============================================================================
# Basics, App and API =========================================================
# =============================================================================


@pytest.fixture()
def test_app():
    """
    Return the Flask app as configured for testing.
    """
    from main import app

    # configure the app for testing
    # SETUP
    app.config["TESTING"] = True

    # CLEAN UP
    yield app


@pytest.fixture()
def api(test_app):
    """
    Initiate the test_client() of the test app, renamed to 'api' so as to avoid
    confusion with client objects.
    """
    return test_app.test_client()


# =============================================================================
# Helper functions for fixtures ===============================================
# =============================================================================


def mock_with_patch(path):
    """
    Return a mock of the given path.
    """
    from unittest.mock import patch

    # A.1
    patcher = patch(path)
    mock = patcher.start()
    return mock


def load_mock_obj_by_id(mock_class, id):
    """
    Create a mock object, mock its id and to_dict() approopriately, and mock
    the given class to return said object upon [Class].load_by_id.
    """
    from unittest.mock import MagicMock

    # 1. create and set up the mock instance
    mock_obj = MagicMock()
    mock_obj.id = id
    mock_obj.to_dict = MagicMock(return_value={"id": id})

    # 2. the mock class to returns the mock instance with load_by_id
    mock_class.load_by_id.return_value = mock_obj
    return mock_obj


# This function is too prescriptive. Rethink the ways its used and decouple them if necessary.
def mock_obj_if_valid_id(is_valid_id, path=None, mock_class=None):
    """
    If valid id, return load_mock_obj_by_id, else mock the class' methods
    load_by_id and load_by_attr to return None, and return None.
    """
    if not path and not mock_class:
        raise ValueError("Either path or mock_class must be provided")

    if path and not mock_class:
        mock_class = mock_with_patch(path)

    if is_valid_id:
        return load_mock_obj_by_id(mock_class, is_valid_id)
    else:
        mock_class.load_by_id.return_value = None
        mock_class.load_by_attr.return_value = None
        return None


def normalized_put_method_name(method):
    """
    Normalize PUT method names into 'PUT'. This is required because PUT-VALID
    and PUT-INVALID are used in the method parameter to inform the
    is_valid_data fixture, allowing the parameterization of both types. Then
    the actual method name must be normalized into a valid http method
    afterwards because it's used by make_request to inform which request to
    make.
    """
    if "PUT" in method or "put" in method:
        method = "PUT"
    return method


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

        if method not in [
            "get",
            "post",
            "put",
            "delete",
            "GET",
            "POST",
            "PUT",
            "DELETE",
        ]:
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


@pytest.fixture(params=[True, False])
def is_authorized(request):
    """
    Parameterizes whether or not the request is authorized, mocks the necessary
    function if so, and returns an authorization token, else returns None.
    """
    # mocking the function used by the authorization wrapper
    mock_get_auth_client = mock_with_patch("authorization.get_client_from_token")
    if request.param:
        mock_get_auth_client.return_value = True
        return str(uuid4())
    else:
        mock_get_auth_client.return_value = None
        return None


@pytest.fixture()
def is_valid_data(request, method):
    """
    Parameterizes whether or not the data for PUT requests is valid. Informed
    by teh method parameter.
    """
    return {"data": "valid data"} if method == "PUT-VALID" else {}


@pytest.fixture(params=[True, False])
def is_valid_id(request):
    """
    Paramererizes whether or not a given object id is valid in the request.
    Mocking the search for said objects must be done in-test, as this fixture
    can not receive an argument for which object is to be mocked from the test.
    """
    return str(uuid4()) if request.param else None
