from db.sql_alchemy import db


class BoilerplateModel(db.Model):
    id = db.Column(db.String(128), primary_key=True, unique=True)
    name = db.Column(db.String(128), unique=True)
    boiler = db.Column(db.String(128))
    plate = db.Column(db.String(128))
    __tablename__ = 'boilerplate_model'

    def __init__(self, *args, **kwargs):
        if not 'id' in kwargs.items():
            from uuid import uuid4
            self.id = str(uuid4())

        boiler = kwargs.get('boiler')
        plate = kwargs.get('plate')
        if boiler and not type(boiler) == str:
            raise ValueError(f'{self.__class__.__name__} boiler must be a string')
        if plate and not type(plate) == str:
            raise ValueError(f'{self.__class__.__name__} plate must be a string')
        
        for k, v in kwargs.items():
            if k == 'id' and not type(k) == str and v:
                raise ValueError(f'{self.__class__.__name__} id must be a uuid4 string')
            self.__dict__[k] = v
    
    def __repr__(self):
        return '<BoilerplateModel %r>' % self.id
    
    def persistent_data(self):
        # this provides behavior tests with
        # more readable language than __dict__
        return dict(self.__dict__)
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def load_by_id(cls, id):
        instance = cls.query.filter_by(id=id).one()
        return instance




if __name__ == '__main__':
    pass
