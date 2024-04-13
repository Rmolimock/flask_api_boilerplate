from models.base import BaseModel, db

class Client(BaseModel):
    '''
    The client model represents clients of the API
    '''
    __tablename__ = 'clients'
    
    name = db.Column(db.String(36), nullable=False)
    token = db.Column(db.String(36), nullable=False)

    def __init__(self, **kwargs):
        '''
        Initialize the client
        '''
        if 'name' not in kwargs:
            raise ValueError('Name is required')
        if 'token' not in kwargs:
            raise ValueError('Token is required')
        
        if not isinstance(kwargs.get('name'), str):
            raise ValueError('Name must be a string')
        if not isinstance(kwargs.get('token'), str):
            raise ValueError('Token must be a string')

        super(Client, self).__init__(**kwargs)

    def __repr__(self):
        '''
        Return the client name
        '''
        return self.name
