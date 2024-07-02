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
def authentication_token():
    return str(uuid4())

@pytest.fixture()
def get_mock_class(mocker):
    def mock_class(mock_class_path):
        """
        Mock a class and return the class object.
        """
        return mocker.patch(mock_class_path)
    return mock_class

'''
parameterize this to have authorization token or not
then use get_mock_class with the route for the client inside before_request
and in here, make it return a magic mock obj with a token that matches the token
or not depending on the request.param. Then anytime a request is sent within a test,
it will do two requests, one with a token and mocked client with the correct client.token
and one with no token sent and a mocked client class that does not return a client object at all.
'''
@pytest.fixture(params=[True, False])
def make_authenticated_request(api, get_mock_class, authentication_token):
    """
    Return a function that can make requests to the API. Optionally includes an authorization header.
    """

    def request(method, route, data=None):
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
        if request.param:
            # will I need access to the token in the test function?
            # I'll need it here to mock a response, and I'll want it in the test
            # function so I can assert that the client was loaded with the correct token
            headers["Authorization"] = f"Bearer {authentication_token}"
            before_client_class = get_mock_class("before_requests.Client")
            attrs = {
                'token': authentication_token,
            }
            mock_client = get_mock_object(before_client_class, **attrs)

        method_func = getattr(api, method)
        return method_func(route, headers=headers, json=data)

    return request


@pytest.fixture()
def get_mock_object(mocker):
    def mock_object(mock_class, obj_id=None, **kwargs):
        """
        Mock a client object and return it.
        """
        mock_obj = mocker.MagicMock()
        if obj_id:
            mock_class.load_by_id.return_value = mock_obj
            mock_obj.id = obj_id
        for key, value in kwargs.items():
            setattr(mock_obj, key, value)
            mock_class.load_by_attr.return_value = mock_obj
        return mock_obj
    return mock_object


@pytest.fixture(params=[True, False])
def has_valid_id(request, mocker, get_mock_class, get_mock_object):

    def is_valid_id(mock_class_path):
        """
        Simulate loading an object with a valid ID. Mock it's class to
        return a mock object when using load_by_id, which has an id equal
        to the string returned by this function, which should be used within
        test functions for requests by id in the route arg of make_request().
        """
        if request.param:
            obj_id = str(uuid4())
            mock_class = get_mock_class(mock_class_path)
            mock_obj = get_mock_object(mock_class, obj_id)
            return obj_id
        else:
            return None
            
    return is_valid_id


@pytest.fixture(params=["get", "post", "put", "delete"])
def method(request):
    return request.param

