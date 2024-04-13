from db import db

class BaseModel(db.Model):
    '''
    Base model for serialization/deserialization and shared methods
    '''
    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True)

    def __init__(self, **kwargs):
        from uuid import uuid4
        from datetime import datetime


        for key, value in kwargs.items():
            setattr(self, key, value)

        if 'id' not in kwargs:
            self.id = str(uuid4())

        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        '''
        Save to the database
        '''
        db.session.add(self)
        db.session.commit()

    def delete(self):
        '''
        Delete from the database
        '''
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def load_all(cls):
        '''
        Load all the objects from the database
        '''
        return cls.query.all()
    
    @classmethod
    def load_all_dict(cls):
        '''
        Load all the objects from the database
        '''
        return [obj.to_dict() for obj in cls.query.all()]

    @classmethod
    def load_by_id(cls, id):
        '''
        Load an object by its id
        '''
        return cls.query.get(id)
    
    def to_dict(self):
        '''
        Serialize the object
        '''
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
