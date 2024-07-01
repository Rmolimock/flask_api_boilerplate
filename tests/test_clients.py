from uuid import uuid4

def test_get_client(has_valid_id, make_request):
    # MOCK VALUES
    valid_client_id = has_valid_id('routes.client.client.Client')

    # SETUP
    invalid_client_id = str(uuid4())
    client_id = valid_client_id if valid_client_id else invalid_client_id

    # ACTION
    response = make_request("get", f"/v1/clients/{client_id}")

    # ASSERTIONS
    assert response.status_code == 200 if valid_client_id else 404
