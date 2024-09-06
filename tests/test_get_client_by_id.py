from authorization import unauthorized_message
from conftest import normalized_put_method_name, mock_with_patch, mock_obj_if_valid_id
import pytest
from uuid import uuid4
from unittest.mock import MagicMock

def mock_put_requests(is_valid_data):
    mock_get_name = mock_with_patch("routes.client.client.get_request_form_attr")
    mock_get_name.return_value = True
    mock_client_class = mock_with_patch("routes.client.client.Client")
    mock_client_class.load_by_attr.return_value = False if is_valid_data else True
    mock_client = mock_obj_if_valid_id(True, mock_client_class)



def test_client_by_id(method, is_valid_id, is_authorized, is_valid_data, make_request):
    """
    Test the /clients/id endpoint with the following parameters:
    - HTTP methods
    - Authorization header
    - Valid and invalid put data
    """

    # SETUP & MOCK ============================================================
    method = normalized_put_method_name(method)

    # only mock finding client by id if is_valid_id
    mock_client_class = mock_with_patch("routes.client.client.Client")
    mock_client = mock_obj_if_valid_id(is_valid_id, mock_client_class)

    client_id = is_valid_id if is_valid_id else str(uuid4())

    # mock updating data in PUT requests
    if method == "PUT" and is_valid_id and is_valid_data:
        mock_put_requests(is_valid_data)
    data = {"name": str(uuid4())} if is_valid_data else {}

    # ACTION ==================================================================
    response = make_request(method, f"/v1/clients/{client_id}/", authorization_header=is_authorized, data=data)


    # ASSERTIONS ==============================================================
    # The order of these conditions is important and aligns with Flask's behavior.

    if not method in ["GET", "PUT", "DELETE"]:
        # method not allowed
        assert response.status_code == 405
        return
    
    if not is_authorized:
        # method allowed but request not authorized
        assert response.status_code == 401
        # assert response.get_json() == unauthorized_message[0]
        return

    if not is_valid_id:
        # method allowed and request authorized but nothing found due to bad id
        assert response.status_code == 404
        return
    
    if method == "PUT":
        if not is_valid_data:
            # method allowed, request authorized, valid id, but put data is invalid
            assert response.status_code == 400
            return        
        else:
            # method allowed, request authorized, valid id, put data valid, updated
            assert response.status_code == 204
            return
    elif method == "DELETE":
        # method allowed, request authorized, valid id, deleted
        assert response.status_code == 204
        return

    # method allowed, request authorized, valid id, GET request
    assert response.status_code == 200
