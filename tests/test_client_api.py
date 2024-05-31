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

    def test_by_id(self, api, method, authorization, mock_client_route):
        # MOCK VALUES / PARAMETERS
        token = authorization.get("header")
        is_authorized = authorization.get("is_authorized")

        # SETUP
        headers = {"Authorization": token}
        client_id = str(uuid4())

        # ACTIONS
        request = getattr(api, method)
        response = request("/v1/clients/{client_id}", headers=headers)

        # ASSERTIONS
        if method == "post":
            assert response.status_code == 405
        elif method == "get":
            assert response.status_code == 200
        else:
            # some tests should have the authorized client.token be the same as the one being requested, and some should not
            # how to parameterize this: if not authorized, don't even bother. If authorized, parameterize the token to be the same or different
            assert response.status_code == 404
        assert is_authorized.called_once_with("id", client_id)
        assert is_authorized.return_value if authorization.get("header") else not is_authorized.return_value
