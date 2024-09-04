import pytest
from authorization import unauthorized_message
from conftest import normalized_put_method_name

def test_all_clients(method, make_request):
    method = normalized_put_method_name(method)

    response = make_request(method, '/v1/clients/')


    if method != 'GET':
        assert response.status_code == 405
        return
    
    assert response.status_code == 200
    assert 'clients' in response.get_json()
    assert isinstance(response.get_json().get('clients'), list)