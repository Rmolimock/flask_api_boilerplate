from uuid import uuid4
import pytest
from unittest.mock import patch
from flask import request


def test_client_method(
    mocker, is_valid_id, method_no_post_put_data, is_authorized, mock_obj_if_valid_id, make_request, mock_obj_if_authorized
):
    
    method = method_no_post_put_data
    if method == 'put-valid':
        method = 'put'
        is_valid_data = {"name": str(uuid4())}
    elif method == 'put-invalid':
        method = 'put'
        is_valid_data = {}

    # MOCK VALUES AND SETUP ===================================================

    # A. [ ] Mocking the search for client by id in GET /v1/clients/{id} ======
    # [X] 1. Client Class is mocked
    # [X] 2. client instance is mocked if is_valid_id
    # [X] 3. client.token matches is_authorized if is_valid_id
    # [X] 4. client.id that matches is_valid_id
    # [X] 5. client.to_dict() that returns a dict of its attributes if is_valid_id (returned as JSON)
    # [ ] 6. client.token matches the request.token in the route if is_valid_id and is_authorized
    # [X] 7. client is returned by Client.load_by_id(id) in the route if is_valid_id
    # [X] 8. Client.load_by_attr(name) returns None if method == "put" and is_valid_name

    # A.1
    client_class_in_route = mocker.patch("routes.client.client.Client")

    # A.2, A.5, A.7
    client_instance_in_route = mock_obj_if_valid_id(client_class_in_route)

    # A.3
    if is_valid_id and is_authorized:
        client_instance_in_route.token = is_authorized

    # A.4
    client_id = client_instance_in_route.id if is_valid_id else str(uuid4())

    # A.8
    if is_valid_id and is_authorized and method == "put" and is_valid_data:
        client_class_in_route.load_by_attr.return_value = None


    # B. [ ] Mocking the search for client by =================================
    #        authorization token in before_requests.py
    # [X] 1. client.token matches is_authorized
    # [X] 2. client is returned by Client.load_by_attr(token) if is_authorized

    client_class_before_request = mocker.patch("before_requests.Client")
    client_instance_before_request = mock_obj_if_authorized(client_class_before_request)
    data = {'name': str(uuid4())} if method == 'put' else {}

    # C. [ ] Mocking the in-route authentication for PUT and DELETE ===========
    # [ ] 1. request.token can not be easily mocked due to request context complications. Must
    #        mock a helper function (get_request_token) that returns it instead. (authenticates in-route rather
    #        than in a wrapper function because the route is shared with GET which is public)
    # [ ] 2. request.form.get('name') must be mocked via a helper function also. (validates
    #        there's no existing client with new name already)

    # C.1 MOCK get_request_token from routes/client/client.py
    mock_get_request_token = mocker.patch("routes.client.client.get_request_token")
    mock_get_request_token.return_value = is_authorized # TODO assert this is done correctly in the right context. Also make sure all my mocks correspond to an assertion.

    # C.2 MOCK get_request_form_attr from routes/client/client.py
    mock_get_request_form_attr = mocker.patch("routes.client.client.get_request_form_attr")
    mock_get_request_form_attr.return_value = data.get("name")

    # ACTION
    response = make_request(method, f"/v1/clients/{client_id}", is_authorized, data)

    # ASSERTIONS

    # Assertions for before_request.py authorization
    if is_authorized and is_valid_id:
        assert client_instance_before_request.token == is_authorized
    client_class_before_request.load_by_attr.assert_called_once_with("token", is_authorized) if is_authorized else None
    
    # Method-specific assertions
    if method == "get":
        assert response.status_code == 200 if is_valid_id else 404
        client_class_in_route.load_by_id.assert_called_once_with(client_id)
        client_instance_in_route.to_dict.assert_called_once() if is_valid_id else None

    elif method == "put":
        if is_valid_data:
            assert response.status_code == 200 if is_valid_id and is_authorized else 401
        else:
            assert response.status_code == 400 if is_valid_id and is_authorized else 401

    elif method == "delete" and is_valid_id and is_authorized:
        assert response.status_code == 204

    else:
        assert response.status_code == 401

    # Assertions for client.py - always called because authorization is checked in the route for this endpoint 
    client_class_in_route.load_by_id.assert_called_once_with(client_id)

