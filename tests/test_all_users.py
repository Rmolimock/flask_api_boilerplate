import pytest
from authorization import unauthorized_message
from conftest import normalized_put_method_name, mock_class_and_object, mock_with_patch

def test_all_users(method, is_authorized, is_valid_post_data, make_request):
    """
    Test the /users endpoint with the following parameters:
    - HTTP methods
    - Authorization header
    - Valid and invalid put data
    """

    # SETUP & MOCK ============================================================
    method = normalized_put_method_name(method)

    mock_has_valid_data = mock_with_patch("routes.user.user.has_valid_data")
    mock_create_user = mock_with_patch("routes.user.user.create_user")

    # if it's a valid POST request, the request should have valid data and user should be created, else no.
    mock_has_valid_data.return_value = is_valid_post_data
    mock_create_user.return_value = is_valid_post_data

    # ACTION ==================================================================

    response = make_request(method, "/v1/users/", authorization=is_authorized, data=is_valid_post_data)

    # ASSERTIONS ==============================================================

    if method not in ["GET", "POST"]:
        assert response.status_code == 405
        return
    
    if not is_authorized:
        assert response.status_code == 401
        assert response.get_json() == unauthorized_message[0]
        return
    
    # must mock the saving of the new user when is_valid_put_data and is_authorized. Create separate function for this.

    if method == "POST":
        if not is_valid_post_data:
            assert response.status_code == 404
            return
        else:
            assert response.status_code == 201
            return

    assert response.status_code == 200
    assert "users" in response.get_json()