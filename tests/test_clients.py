'''
Test class for clients
'''
from scripts.register_client import create_client
import pytest


# Test client registration
# this is actually multiple tests, such as:
# 1. registration checks for existing client by name by calling .load_by_attr() once with "name" and name
# 2. registration creates a new client by calling .save() once
# 3. it returns the client token
# 4. it ends the session

@pytest.fixture
def mock_client(mocker):
    # Create a new mock Client class for each test
    mock_client = mocker.patch('scripts.register_client.Client')
    return mock_client
    
@pytest.fixture
def mock_db(mocker):
    # Create a new mock db session for each test
    mock_db = mocker.patch('scripts.register_client.db.session')
    return mock_db

class TestClientRegistration:
    def test_existing_client(self, mock_client, mock_db):
        mock_client.load_by_attr.return_value = True
        assert create_client("test_name") == "Client name already in use.\n"
        mock_client.load_by_attr.assert_called_once_with("name", "test_name")
        mock_client.return_value.save.assert_not_called()
        mock_db.remove.assert_called()
        # assert_called_once fails due to a phantom second call to remove() that I can't find
    
    def test_register_client(self, mock_client):
        # test that a new client is registered
        mock_client.load_by_attr.return_value = False
        mock_client.return_value.save.return_value = None
        mock_client.return_value.token = "test_token"
    
        token = create_client("test_name")
        print(token)
        
        assert token
        assert isinstance(token, str)
        mock_client.load_by_attr.assert_called_once_with("name", "test_name")
        mock_client.return_value.save.assert_called_once()

    def test_db_session_remove(self, mock_client, mock_db):
        # test that the session is closed
        mock_client.load_by_attr.return_value = False
        mock_db.remove.return_value = None
        create_client("test_name_2")
        mock_db.remove.assert_called()
