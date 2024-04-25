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

class TestClientRegistration:
    @pytest.fixture(autouse=True, scope="function")
    def setup(self, mocker):
        self.mock_client_load_by_attr = mocker.patch("scripts.register_client.Client.load_by_attr")
        self.mock_client_save = mocker.patch("scripts.register_client.Client.save")
        self.mock_db_session_remove = mocker.patch("scripts.register_client.db.session.remove")
        yield # a shortcut for teardown code
        self.mock_client_load_by_attr.reset_mock()
        self.mock_client_save.reset_mock()
        self.mock_db_session_remove.reset_mock()
    
    def test_existing_client(self):
        # test that an existing client is not registered
        self.mock_client_load_by_attr.return_value = True

        assert create_client("test_name") == "Client name already in use.\n"
        self.mock_client_load_by_attr.assert_called_once_with("name", "test_name")
        self.mock_client_save.assert_not_called()
        self.mock_db_session_remove.assert_called_once()
    
    def test_register_client(self):
        # test that a new client is registered
        self.mock_client_load_by_attr.return_value = False
        self.mock_client_save.return_value = True
        token = create_client("test_name")
        
        assert token
        assert isinstance(token, str)
        self.mock_client_load_by_attr.assert_called_once_with("name", "test_name")
        self.mock_client_save.assert_called_once()
    
    def test_db_session_remove(self):
        # test that the session is closed
        self.mock_client_load_by_attr.return_value = False
        self.mock_db_session_remove.return_value = True
        create_client("test_name_2")
        self.mock_db_session_remove.assert_called_once()
