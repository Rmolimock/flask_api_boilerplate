from models.base_model import BaseModel, db


class User(BaseModel):

    __tablename__ = "users"

    name = db.Column(db.String(36), nullable=False, unique=True)

    def __init__(self, **kwargs):
        """
        Initialize the user
        """

        # ensure the user has a name and it is a string
        name = kwargs.get("name")

        if not name:
            raise ValueError("Name is required")

        if not isinstance(name, str):
            raise TypeError("Name must be a string")

        # check if the user already exists
        existing_user = User.load_by_attr("name", name)
        if existing_user:
            raise ValueError("User already exists")

        super(User, self).__init__(**kwargs)

    def __repr__(self):
        """
        Return the user name
        """
        return self.name
