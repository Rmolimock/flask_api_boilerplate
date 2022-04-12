def database_factory(app, orm_type):
    if orm_type == 'flask_sqlalchemy':
        # might add an option for (non-flask) sqlalchemy in the future
        from flask_sqlalchemy import SQLAlchemy            
        db = SQLAlchemy(app)
        return db
    else:
        return None
