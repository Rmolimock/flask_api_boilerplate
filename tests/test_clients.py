from uuid import uuid4
import pytest


def test_client_method(
    mocker, is_valid_id, method_no_post, mock_obj_if_valid_id, make_request
):
    # MOCK VALUES
    client_class_in_route = mocker.patch("routes.client.client.Client")
    method = method_no_post

    # SETUP
    client_instance_in_route = mock_obj_if_valid_id(client_class_in_route)
    client_id = client_instance_in_route.id if is_valid_id else str(uuid4())

    # ACTION
    response = make_request(method, f"/v1/clients/{client_id}")

    # ASSERTIONS
    if method == "get":

        assert response.status_code == 200 if is_valid_id else 404
        client_class_in_route.load_by_id.assert_called_once_with(client_id)
        client_instance_in_route.to_dict.assert_called_once() if is_valid_id else None
    else:

        assert response.status_code == 401
    client_class_in_route.load_by_id.assert_called_once_with(client_id)


"""
authorizing_client = get_mock_class("before_requests.Client")
attrs = {
    'token': authorization_token,
}
authenticated_client = get_mock_object(authorizing_client, **attrs)
"""
"""
if authorized:
    print("Checking authorizing_client.load_by_attr calls")
    print(f"Authorizing client mock after request: {authorizing_client}")
    print(f"Mock calls: {authorizing_client.load_by_attr.mock_calls}")
    authorizing_client.load_by_attr.assert_called_once_with("token", authorization_token)
    assert authenticated_client.token == authorization_token
"""
