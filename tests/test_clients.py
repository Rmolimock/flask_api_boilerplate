from uuid import uuid4
from unittest.mock import patch
from conftest import mock_obj_if_valid_id, mock_obj_if_authorized, mock_with_patch


def mock_client_in_route(is_valid_id, is_authorized, method, is_valid_data):

    client_class_in_route = mock_with_patch("routes.client.client.Client")

    # A.2, A.3, A.4, A.5
    client_instance_in_route = mock_obj_if_valid_id(is_valid_id, client_class_in_route)

    # A.6
    if is_valid_id and is_authorized:
        client_instance_in_route.token = is_authorized

    # A.9
    # ex: client name already taken
    client_class_in_route.load_by_attr.return_value = client_instance_in_route
    # valid PUT data, meaning client name is unique
    if method == "put" and is_valid_id and is_authorized and is_valid_data:
        client_class_in_route.load_by_attr.return_value = None

    return client_class_in_route, client_instance_in_route


def mock_route_helpers(is_valid_data, is_valid_id, is_authorized, method):
    # A.7
    mock_get_request_token = mock_with_patch("routes.client.client.get_request_token")
    mock_get_request_token.return_value = is_authorized

    # A.8
    mock_get_request_form_attr = mock_with_patch("routes.client.client.get_request_form_attr")

    mock_get_request_form_attr.return_value = None

    if method == "put" and is_valid_id and is_authorized:
        mock_get_request_form_attr.return_value = is_valid_data.get("name")

    return mock_get_request_token, mock_get_request_form_attr


def test_clients_by_id(
    is_valid_id,
    method_no_post_put_data,
    is_authorized,
    is_valid_data,
    make_request,
):
    method = method_no_post_put_data
    if "put" in method:
        method = "put"

    # =========================================================================
    # MOCK VALUES AND SETUP ===================================================
    # =========================================================================

    # A.  [X] IN ROUTE - Mocking the search for client by id in GET /v1/clients/{id} ======

    # The code always enters the route because it's shared between authorized and unauthorized requests.
    # GET does not require authorization, but PUT and DELETE do, which means they must check that the
    # client.token matches the request.token manually, rather than relying on a wrapper function to do so.

    # [X] [X] Mocked | Asserted (if applicable)
    # [X]     1. Client Class is mocked
    # [X]     2. client instance is mocked if is_valid_id
    # [X] [X] 3. client instance is returned by Client.load_by_id(id) if is_valid_id
    # [X] [X] 4. client.id matches is_valid_id if is_valid_id
    # [X] [X] 5. client.to_dict() returns a dict of its attributes if is_valid_id (returned as JSON)
    # [X] [X] 6. client.token matches is_authorized if is_valid_id
    # [X] [X] 7. request.token matches is_authorized if is_valid_id
    # [X] [X] 8. get_request_form_attr returns is_valid_data.get("name") if method == "put"
    # [X] [X] 9. Client.load_by_attr(name) returns None if method == "put" and is_valid_name and is_authorized
    # [X] [X] 10. Use is_valid_id for request if present, else dummy id

    # A.1 - A.6, A.9
    client_class_in_route, client_instance_in_route = mock_client_in_route(
        is_valid_id, is_authorized, method, is_valid_data
    )

    mock_get_request_token, mock_get_request_form_attr = mock_route_helpers(
        is_valid_data, is_valid_id, is_authorized, method
    )

    # A.10
    client_id = client_instance_in_route.id if is_valid_id else str(uuid4())


    # B.  [X] IN BEFORE_REQUESTS.py - Mocking the search for client by =========
    # [X] [X] Mocked | Asserted (if applicable)
    #        authorization token in before_requests.py
    # [X]     1. Client class is mocked
    # [X]     2. client instance is mocked if is_authorized
    # [X] [X] 3. client instance is returned by Client.load_by_attr(token) if is_authorized
    # [X] [X] 4. client.token matches is_authorized

    # B.1
    patcher = patch("before_requests.Client")
    client_class_before_request = patcher.start()

    # B.2, B.3, B.4
    client_instance_before_request = mock_obj_if_authorized(is_authorized, client_class_before_request)


    # =========================================================================
    # ACTION ==================================================================
    # =========================================================================

    response = make_request(method, f"/v1/clients/{client_id}", is_authorized, is_valid_data)


    # =========================================================================
    # ASSERTIONS ==============================================================
    # =========================================================================

    # Assertions for authorization

    # In-route
    # A.6
    assert client_instance_in_route.token == is_authorized if is_authorized and is_valid_id else True

    # A.7
    assert mock_get_request_token.return_value == is_authorized if is_authorized and is_valid_id else True

    # In before_request.py
    # B.3
    assert client_class_before_request.load_by_attr.return_value == client_instance_before_request if is_authorized else True

    # B.4
    client_class_before_request.load_by_attr.assert_called_once_with("token", is_authorized) if is_authorized else None
    assert client_instance_before_request.token == is_authorized if is_authorized else True

    # Always called
    # A.10
    assert client_id == is_valid_id if is_valid_id else True

    # A.3, A.4
    client_class_in_route.load_by_id.assert_called_once_with(client_id)
    if is_valid_id:
        assert client_instance_in_route.id == client_id == is_valid_id
        assert client_class_in_route.load_by_id.return_value == client_instance_in_route
    else:
        assert client_instance_in_route is None
        assert client_class_in_route.load_by_id.return_value is None

    # Method-specific assertions
    if method == "get":
        assert response.status_code == 200 if is_valid_id else 404
        # A.5
        client_instance_in_route.to_dict.assert_called_once() if is_valid_id else None

    elif method == "put":
        # A.8
        mock_get_request_form_attr.assert_called_once() if is_valid_id and is_authorized else None
        assert mock_get_request_form_attr.return_value == is_valid_data.get("name") if is_valid_id and is_authorized else True

        # A.9
        client_class_in_route.load_by_attr.assert_called_once_with("name", is_valid_data.get("name")) if is_valid_id and is_authorized and is_valid_data else None
        assert response.status_code == 400 if is_valid_id and is_authorized and not is_valid_data else True

        if is_valid_data:
            assert response.status_code == 200 if is_valid_id and is_authorized else 401
            # A.5
            client_instance_in_route.to_dict.assert_called_once() if is_valid_id and is_authorized else None
        else:
            assert client_class_in_route.load_by_attr.return_value == client_instance_in_route
            if is_valid_id and not is_authorized:
                assert response.status_code == 401
            elif is_valid_id and is_authorized:
                assert response.status_code == 400
            elif not is_valid_id and not is_authorized:
                assert response.status_code == 404
            elif not is_valid_id and is_authorized:
                assert response.status_code == 404

    elif method == "delete":
        if is_valid_id and is_authorized:
            assert response.status_code == 204
        if is_valid_data and not is_authorized:
            assert response.status_code == 401
        if not is_valid_id:
            assert response.status_code == 404
    else:
        assert response.status_code == 401
