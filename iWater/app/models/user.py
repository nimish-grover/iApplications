from iWater.app.db import db
from flask_login import UserMixin

class UserModel(UserMixin, db.Model): 
    __tablename__ = "users"

    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(80), unique=True, nullable=False)
    email=db.Column(db.String(),unique=True,nullable = False)
    password=db.Column(db.String(), nullable=False)

    def __init__(self, username, email, password):
        self.password = password
        self.username = username
        self.email = email
        
    def json(self):
        return{
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'email': self.email
        }
    
    @classmethod
    def find_by_username(cls, username):
        query = cls.query.filter_by(username=username).first()
        return query.json()
    
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

    # Class method to get a user by email
    @classmethod
    def get_user_by_email(cls, _email):
        query = cls.query.filter_by(email=_email).first()
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