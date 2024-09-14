import pytest
from authorization import unauthorized_message
from conftest import normalized_put_method_name, mock_class_and_object, mock_with_patch

def test_all_users(method, is_authorized, is_valid_data, make_request):
    """
    Test the /users endpoint with the following parameters:
    - HTTP methods
    - Authorization header
    - Valid and invalid put data
    """

    method = normalized_put_method_name(method)

    mock_has_valid_data = mock_with_patch("routes.user.user.has_valid_data") # validate at high level,
    # don't get bogged down in mocking details here.
    mock_has_valid_data.return_value = is_valid_data

    response = make_request(method, "/v1/users/", authorization=is_authorized, data=is_valid_data)

    if method not in ["GET", "POST"]:
        assert response.status_code == 405
        return
    
    if not is_authorized:
        assert response.status_code == 401
        assert response.get_json() == unauthorized_message[0]
        return
    
    # need to use a different is_valid_data method. That one is coupled to the PUT method. It will never be POST and valid_data.

    if method == "POST":
        if not is_valid_data:
            assert response.status_code == 404
            return
        else:
            assert response.status_code == 201
            assert "client_id" in response.get_json()
            return

    assert response.status_code == 200
    assert "users" in response.get_json()