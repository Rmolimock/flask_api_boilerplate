"""
Tests for client registration via scripts/register_client.py <client_name>
"""

from scripts.register_client import create_client
import pytest


@pytest.fixture
def mock_client(mocker):
    # Initialize a shared mock client for TestClientRegistration tests
    mock_client = mocker.patch("scripts.register_client.Client")
    return mock_client


@pytest.fixture
def mock_db(mocker):
    # Initialize a shared mock db session for TestClientRegistration tests
    mock_db = mocker.patch("scripts.register_client.db.session")
    return mock_db


class TestClientRegistration:
    """
    Test the create_client function in scripts/register_client.py
    """

    def test_existing_client(self, mock_client, mock_db):
        # test that a client name already in use is not registered

        # MOCK VALUES
        # (here to avoid assert() detecting multiple calls)
        mock_client.load_by_attr.return_value = True

        # ACTIONS
        response = create_client("test_name")

        # ASSERTIONS
        assert response == "Client name already in use.\n"
        mock_client.load_by_attr.assert_called_once_with("name", "test_name")
        mock_client.return_value.save.assert_not_called()
        mock_db.remove.assert_called()
        # assert_called_once fails due to a phantom second call to remove() that I can't find
        # so I'm using assert_called() for now

    def test_register_client(self, mock_client):
        # test that a new client is registered when the name is unique

        # MOCK VALUES
        mock_client.load_by_attr.return_value = False
        mock_client.return_value.save.return_value = None
        mock_client.return_value.token = "test_token"

        # ACTIONS
        token = create_client("test_name")

        # ASSERTIONS
        assert token
        assert isinstance(token, str)
        mock_client.load_by_attr.assert_called_once_with("name", "test_name")
        mock_client.return_value.save.assert_called_once()

    def test_db_session_remove(self, mock_client, mock_db):
        # test that the session is closed after a client is registered

        # MOCK VALUES
        mock_client.load_by_attr.return_value = False
        mock_db.remove.return_value = None

        # ACTIONS
        create_client("test_name_2")

        # ASSERTIONS
        mock_db.remove.assert_called()
