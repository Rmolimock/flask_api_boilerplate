from uuid import uuid4


def test_get_client(has_valid_id, make_request, get_mock_class, method, authentication_token, get_mock_object):
    # MOCK VALUES
    client_class_route = 'routes.client.client.Client'
    valid_client_id = has_valid_id(client_class_route)
    authenticator_class = get_mock_class("before_requests.Client")
    attrs = {
        'token': authentication_token,
    }
    authenticated_client = get_mock_object(client_class_route, **attrs)



    # get_mock_class returns the same mocked client class used by has_valid_id
    # so I can assert it was called with the correct client id
    mock_client_class = get_mock_class(client_class_route)

    # SETUP
    invalid_client_id = str(uuid4())
    client_id = valid_client_id if valid_client_id else invalid_client_id

    # ACTION
    response = make_request(method, f"/v1/clients/{client_id}")

    # ASSERTIONS
    if method == "post":
        assert response.status_code == 405
        return
    assert response.status_code == 200 if valid_client_id else 404
    mock_client_class.load_by_id.assert_called_once_with(client_id)
    authenticator_class.load_by_attr.assert_called_once_with("token", authentication_token)
    assert authenticated_client.token == authentication_token
