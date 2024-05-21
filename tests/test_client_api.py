import pytest


class TestClients:
    def test_get_all_clients(self, api, authorization):
        # MOCK VALUES
        headers = {'Authorization': authorization} if authorization else {}
        # ACTIONS
        response = api.get("/v1/clients/", headers=headers)

        # ASSERTIONS
        assert response.status_code == 200

    def test_by_id(self, api, authorization):
        pass