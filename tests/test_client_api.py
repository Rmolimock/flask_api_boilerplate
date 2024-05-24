import pytest
from uuid import uuid4


class TestClients:
    def test_get_all_clients(self, api, authorization):
        # MOCK VALUES
        headers = {"Authorization": authorization} if authorization else {}
        # ACTIONS
        response = api.get("/v1/clients/", headers=headers)

        # ASSERTIONS
        assert response.status_code == 200

    def test_by_id(self, api, method, mock_client_before_request, authorization):
        # MOCK VALUES
        headers = {"Authorization": authorization} if authorization else {}
        client_id = str(uuid4())
        # ACTIONS
        request = getattr(api, method)
        response = request("/v1/clients/{client_id}", headers=headers)
        # ASSERTIONS
        if method == "post":
            assert response.status_code == 405
        else:
            assert response.status_code == 404
        if authorization and mock_client_before_request:
            assert mock_client_before_request.load_by_id.called_once_with(client_id)
