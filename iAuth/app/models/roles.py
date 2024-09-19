from iAuth.app.db import db

class RolesModel(db.Model): 
    __tablename__ = "roles"

    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(80),nullable=False)
    type=db.Column(db.String(),nullable = False)

    def __init__(self, name, type):
        self.name = name
        self.type = type
        
    def json(self):
        return{
            'id': self.id,
            'name': self.name,
            'type': self.type
        }
    
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
    
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    
    @classmethod
    def get_user_by_id(cls, _id):
        query = cls.query.filter_by(id=_id).first()
        if query:
            return query.json()
        else:
            return None

    # Class method to get a user by type
    @classmethod
    def get_user_by_type(cls, _type):
        query = cls.query.filter_by(type=_type).first()
        if query:
            return query.json()
        else:
            return None

    # Class method to get all users
    @classmethod
    def get_all(cls):
        query = cls.query.order_by(cls.id.desc())
        return query

    # Method to save the user object to the database
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # Class method to delete a user from the database by ID
    @classmethod
    def delete_from_db(cls, _id):
        user = cls.query.filter_by(id=_id).first()
        db.session.delete(user)
        db.session.commit()

    # Method to commit changes to the database
    def commit_db():
        db.session.commit()

    # Class method to update user information in the database by ID
    @classmethod
    def update_db(cls, data, _id):
        user = cls.query.filter_by(id=_id).update(data)
        db.session.commit()