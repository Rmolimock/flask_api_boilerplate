from models.base_model import BaseModel, db


class User(BaseModel):

    __tablename__ = "users"

    name = db.Column(db.String(36), nullable=False)
    handle = db.Column(db.String(36), nullable=False, unique=True)

    def __init__(self, **kwargs):
        """
        Initialize the user
        """

        # ensure the user has a name and handle, and they are strings
        name = kwargs.get("name")
        handle = kwargs.get("handle")

        if not (name and handle):
            raise ValueError("Name and handle are required")

        if not isinstance(name, str):
            raise TypeError("Name must be a string")

        if not isinstance(handle, str):
            raise TypeError("Handle must be a string")

        # check if the user already exists
        name_taken = User.load_by_attr("name", name)
        if name_taken:
            raise ValueError("User name is taken")

        handle_taken = User.load_by_attr("handle", handle)
        if handle_taken:
            raise ValueError("User handle is taken")

        super(User, self).__init__(**kwargs)

    def __repr__(self):
        """
        Return the user name
        """
        return self.name
