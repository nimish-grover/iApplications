  # Import the database extension
from datetime import datetime
import pytz
from sqlalchemy import distinct, extract, func, and_, or_  # Import various SQL functions
from flask_login import UserMixin
import uuid

from iSaksham.app.db import db  # Import UserMixin for user management


class User(UserMixin, db.Model):  # Define the User class inheriting from UserMixin and db.Model
    def get_uuid():
        return str(uuid.uuid4())
    
    __tablename__ = "user"  # Define the table name in the database
    
    # Define columns of the table
    id = db.Column(db.Integer, primary_key=True)  # Primary key column
    name = db.Column(db.String(128))  # Name column, unique constraint applied
    email = db.Column(db.String(128),unique=True)  # Email column
    password = db.Column(db.String(128))  # Password column
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    registered_on = db.Column(db.DateTime, default=lambda: datetime.now(tz=pytz.timezone('Asia/Kolkata')))
    uuid = db.Column(db.String(36), unique=True, index=True,default=get_uuid)
    activity_log = db.relationship('ActivityLog', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    # Constructor to initialize the User object
    def __init__(self, name, email, password,is_active,is_admin,_uuid=None,registered_on=None):
        if _uuid is None:
            _uuid = str(uuid.uuid4())
        if registered_on is None:
            registered_on = datetime.now(tz=pytz.timezone('Asia/Kolkata'))
            
        self.is_active=is_active
        self.is_admin=is_admin
        self.registered_on = registered_on
        self.uuid = _uuid
        self.password = password
        self.name = name
        self.email = email

    # Method to represent User object as JSON
    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'uuid':self.uuid,
            'registered_on':self.registered_on,
            'is_active':self.is_active,
            'is_admin':self.is_admin
        }

    # Class method to get a user by ID
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
