import pytest
from uuid import uuid4


def test_user_by_id(is_valid_id, method_no_post_put_data, is_authorized, mock_obj_if_valid_id, make_request, mocker):
    # =========================================================================
    # MOCK VALUES AND SETUP ===================================================
    # =========================================================================

    # A.  [ ] Mocked | Asserted (if applicable)
    # [ ]     1. User Class is mocked
    # [ ]     2. user instance is mocked if is_valid_id
    # [ ] [ ] 3. user instance is returned by User.load_by_id(id) if is_valid_id
    # [ ] [ ] 4. user.id matches is_valid_id if is_valid_id
    # [ ] [ ] 5. user.to_dict() returns a dict of its attributes if is_valid_id (returned as JSON)
    # [ ] [ ] 6. user.token matches is_authorized if is_valid_id -
    # [ ] [ ] 7. request.token matches is_authorized if is_valid_id - these two I can change to some authorized wrapper
    # [ ] [ ] 8. get_request_form_attr returns is_valid_data.get("name") if method
    method = method_no_post_put_data
    if 'put' in method:
        method = 'put'

    # A.1
    user_class = mocker.patch("routes.user.user.User")

    # A.2, A.3, A.4, A.5
    mock_user = mock_obj_if_valid_id(user_class)

    # mock authorization wrapper here

    user_id = is_valid_id if is_valid_id else str(uuid4())

    response = make_request(method, f"/v1/users/{user_id}", is_authorized)

    assert response.status_code == 401
    if is_valid_id and is_authorized:
        # once authorization wrapper is mocked, assert 200 here
        pass
    assert response.status_code != 200