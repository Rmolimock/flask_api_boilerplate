from models.base import BaseModel, db
from models.client import Client

class User(BaseModel):
    """
    Users of the app, associated with a given client.
    """
    __tablename__ = "users"

    # client_id associated with a client model
    client_id = db.Column(db.String(36), db.ForeignKey("clients.id"), nullable=False)
    client = db.relationship("Client", backref=db.backref("users"))

    name = db.Column(db.String(36), nullable=False)
    email = db.Column(db.String(36), nullable=False)

    def __init__(self, **kwargs):
        client_id = kwargs.get("client_id")
        if not client_id:
            raise ValueError("Client ID is required")
        
        if not kwargs.get("name"):
            raise ValueError("User name is required")
        
        if not kwargs.get("email"):
            return ValueError("User email is required")
        
        client_valid = Client.load_by_id(client_id)

        if not client_valid:
            raise ValueError("Invalid client ID")
        
        self.client_id = client_id
        self.client = client_valid
        self.name = kwargs.get("name")
        self.email = kwargs.get("email")

        super(User, self).__init__(**kwargs)

    def __repr__(self):
        return self.name