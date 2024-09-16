from authorization import unauthorized_message
from conftest import normalized_put_method_name, mock_with_patch, mock_resource
import pytest
from uuid import uuid4
from unittest.mock import MagicMock


def test_user_by_id(method, is_valid_id, is_authorized, is_valid_put_data, make_request, mock_resource):
    
    # SETUP & MOCK ============================================================
    method = normalized_put_method_name(method)

    mock_class, mock_obj = mock_resource("routes.user.user.User")

    user_id = is_valid_id if is_valid_id else str(uuid4())

    get_attr_from_request_form = mock_with_patch("routes.user.user.get_attr_from_request_form")
    get_attr_from_request_form.return_value = False
    if method == "PUT" and is_valid_id and is_authorized and is_valid_put_data:
        get_attr_from_request_form.return_value = True 

    # ACTION ==================================================================

    response = make_request(method, f"/v1/users/{user_id}/", authorization=is_authorized)

    # ASSERTIONS ==============================================================

    if method not in ["GET", "DELETE", "PUT"]:
        assert response.status_code == 405
        return

    if not is_authorized:
        assert response.status_code == 401
        return

    if not is_valid_id:
        assert response.status_code == 404
        return
    
    if method == "PUT":
        if not is_valid_put_data:
            assert response.status_code == 400
        else:
            assert response.status_code == 204
        return
    
    if method == "DELETE":
        assert response.status_code == 204
        return

    assert response.status_code == 200
