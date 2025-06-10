from iAuth.app.db import db
from flask_login import UserMixin
from iAuth.app.models.roles import RolesModel

class inRoleModel(db.Model): 
    __tablename__ = "in_role"

    id=db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    
    def __init__(self, user_id, role_id):

        self.user_id = user_id
        self.role_id = role_id
        
    def json(self):
        return{
            'id': self.id,
            'user_id': self.user_id,
            'role_id': self.role_id
        }
    
    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()
    
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    
    @classmethod
    def get_role_by_id(cls, _user_id):
        role = db.session.query(RolesModel.name) \
        .join(inRoleModel, RolesModel.id == inRoleModel.role_id) \
        .filter(inRoleModel.user_id == _user_id).first()
        if role:
            return role.name
        else:
            return None

    # Class method to get a user by role_id
    @classmethod
    def get_user_by_role_id(cls, _role_id):
        query = cls.query.filter_by(role_id=_role_id).first()
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