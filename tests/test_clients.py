from uuid import uuid4
import pytest


def test_client_methods(has_valid_id, method_no_post, make_request, get_mock_class, get_mock_object):
    # MOCK VALUES
    client_class_route = 'routes.client.client.Client'
    valid_client_id = has_valid_id(client_class_route) # a parameter
    '''
    authorizing_client = get_mock_class("before_requests.Client")
    attrs = {
        'token': authorization_token,
    }
    authenticated_client = get_mock_object(authorizing_client, **attrs)
    '''
    # get_mock_class returns the same mocked client class used by has_valid_id
    # so I can assert it was called with the correct client id
    mock_client_class = get_mock_class(client_class_route)

    # SETUP
    invalid_client_id = str(uuid4())
    print('is valid:', valid_client_id, 'invalid:', invalid_client_id)

    client_id = valid_client_id if valid_client_id else invalid_client_id

    # ACTION
    response = make_request(method_no_post, f"/v1/clients/{client_id}")

    # ASSERTIONS
    if method_no_post == 'get':
        assert response.status_code == 200 if valid_client_id else 404
    else:
        assert response.status_code == 401
    mock_client_class.load_by_id.assert_called_once_with(client_id)
    # if authorization header was present:
    '''
    if authorized:
        print("Checking authorizing_client.load_by_attr calls")
        print(f"Authorizing client mock after request: {authorizing_client}")
        print(f"Mock calls: {authorizing_client.load_by_attr.mock_calls}")
        authorizing_client.load_by_attr.assert_called_once_with("token", authorization_token)
        assert authenticated_client.token == authorization_token
    '''