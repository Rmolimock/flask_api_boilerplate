import pytest
from authorization import unauthorized_message


def test_status(make_request, method, is_authorized, is_valid_data):
    if 'PUT' in method:
        method = 'PUT'
    response = make_request(method, '/status', data=is_valid_data, authorization_header=is_authorized)

    if method == 'GET' and not is_authorized:
        assert response.status_code == 401
        assert response.get_json() == unauthorized_message[0]
    elif method == 'GET' and is_authorized:
        assert response.status_code == 200
        assert response.get_json() == {'message': 'OK'}
    else:
        assert response.status_code == 405