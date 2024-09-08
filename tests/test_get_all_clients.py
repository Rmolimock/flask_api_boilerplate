import pytest
from authorization import unauthorized_message
from conftest import normalized_put_method_name


def test_all_clients(method, is_authorized, is_valid_data, make_request):
    """
    Test the /clients endpoint with the following parameters:
    - HTTP methods
    - Authorization header
    - Valid and invalid put data
    """

    # SETUP & MOCK ============================================================
    method = normalized_put_method_name(method)

    response = make_request(
        method, "/v1/clients/", data=is_valid_data, authorization_header=is_authorized
    )

    if method != "GET":
        assert response.status_code == 405
        return

    if not is_authorized:
        assert response.status_code == 401
        assert response.get_json() == unauthorized_message[0]
        return

    assert response.status_code == 200
    assert "clients" in response.get_json()
    assert isinstance(response.get_json().get("clients"), list)