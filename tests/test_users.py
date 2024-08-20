import pytest
from uuid import uuid4
from conftest import mock_obj_if_valid_id, mock_obj_if_authorized, mock_with_patch, mock_class_load_if_valid_put_data


def test_user_by_id(is_valid_id, method_no_post_put_data, is_authorized, make_request, mocker):
    # =========================================================================
    # MOCK VALUES AND SETUP ===================================================
    # =========================================================================

    # A.  [ ] Mocked | Asserted (if applicable)
    # [X]     1. User Class is mocked
    # [X]     2. user instance is mocked if is_valid_id
    # [X] [X] 3. user instance is returned by User.load_by_id(id) if is_valid_id
    # [X] [X] 4. user.id matches is_valid_id if is_valid_id
    # [X] [X] 5. user.to_dict() returns a dict of its attributes if is_valid_id (returned as JSON)
    # [ ] [ ] 6. user.token matches is_authorized if is_valid_id -
    # [ ] [ ] 7. request.token matches is_authorized if is_valid_id - these two I can change to some authorized wrapper
    # [ ] [ ] 8. get_request_form_attr returns is_valid_data.get("name") if method
    method = method_no_post_put_data
    if 'put' in method:
        method = 'put'

    # A.1
    mock_user_class = mock_with_patch("routes.user.user.User")

    # A.2, A.3, A.4, A.5
    mock_user = mock_obj_if_valid_id(is_valid_id, mock_user_class)
    if mock_user:
        mock_user.token = is_authorized
    # ---
    # mock authorization wrapper here

    user_id = is_valid_id if is_valid_id else str(uuid4())

    response = make_request(method, f"/v1/users/{user_id}", is_authorized)

    assert mock_user_class.load_by_id.called_once_with(user_id)
    if is_valid_id:
        assert mock_user_class.load_by_id.return_value != None
        assert mock_user.id == is_valid_id
        assert is_valid_id == user_id
        assert mock_user.to_dict.called_once()
    else:
        assert mock_user_class.load_by_id.return_value == None
    assert response.status_code == 401
    if is_valid_id and is_authorized:
        # once authorization wrapper is mocked, assert 200 here
        assert mock_user.token == is_authorized # this isn't really testing anything in the code itself
    assert response.status_code != 200