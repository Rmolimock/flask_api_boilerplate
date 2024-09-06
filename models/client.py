from models.base import BaseModel, db


class Client(BaseModel):
    """
    The client model represents clients of the API
    """

    __tablename__ = "clients"

    name = db.Column(db.String(36), nullable=False, unique=True)
    token = db.Column(db.String(36), nullable=False)

    def __init__(self, **kwargs):
        """
        Initialize the client. Create a unique token for authorization.
        """
        from uuid import uuid4

        # ensure the client has a name and it is a string
        if "name" not in kwargs:
            raise ValueError("Name is required")

        name = kwargs.get("name")

        if not isinstance(name, str):
            raise TypeError("Name must be a string")

        # check if the client already exists
        name_taken = Client.load_by_attr("name", name)
        if name_taken:
            raise ValueError("Client already exists")

        # do not allow clients to create their own tokens
        if "token" in kwargs:
            del kwargs["token"]

        # create a unique token for the client
        token = str(uuid4())
        self.token = token

        super(Client, self).__init__(**kwargs)

    def __repr__(self):
        """
        Return the client name
        """
        return self.name
