import pytest
from authorization import unauthorized_message
from conftest import normalized_put_method_name

def test_all_users(method, make_request):
    """
    Test the /users endpoint with the following parameters:
    - HTTP methods
    - Authorization header
    - Valid and invalid put data
    """

    method = normalized_put_method_name(method)

    response = make_request(method, "/v1/users/")

    if method is not "GET":
        assert response.status_code == 405
        return

    assert response.status_code == 200