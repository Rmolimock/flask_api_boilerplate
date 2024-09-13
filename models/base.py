from db import db


class BaseModel(db.Model):
    """
    Base model for serialization/deserialization and shared methods
    """

    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, **kwargs):
        from uuid import uuid4
        from datetime import datetime

        for key, value in kwargs.items():
            setattr(self, key, value)

        if "id" not in kwargs:
            self.id = str(uuid4())

        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """
        Save to the database
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        Delete from the database
        """
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def load_all(cls):
        """
        Load all the objects from the database
        """
        return db.session.query(cls).all()

    @classmethod
    def load_all_dict(cls, remove_attr=None):
        """
        Load all the objects from the database. Optionally remove an attribute from the response.
        """
        return [
        {k: v for k, v in obj.to_dict().items() if k != remove_attr} 
        for obj in cls.load_all()
        ]

    @classmethod
    def load_by_id(cls, id):
        """
        Load an object by its id
        """
        return db.session.get(cls, id)

    @classmethod
    def load_by_attr(cls, attr, value):
        """
        Load an object by an attribute and its value
        """
        return db.session.query(cls).filter(getattr(cls, attr) == value).first()

    def to_dict(self):
        """
        Serialize the object
        """
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }
