from flask_login import UserMixin
from iJal.app.db import db
from passlib.hash import pbkdf2_sha256

from iJal.app.models.states import State

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(300))
    state_id = db.Column(db.Integer, db.ForeignKey("states.id"), nullable=False)
    isActive = db.Column(db.Boolean, nullable=False, default=False)
    isAdmin = db.Column(db.Boolean, nullable=False, default=False)

    state = db.relationship("State", backref=db.backref('users', lazy='dynamic'))

    def __init__(self, username, password, state_id, isActive, isAdmin):
        self.username = username
        self.password = password
        self.isActive = isActive
        self.isAdmin = isAdmin
        self.state_id = state_id

    def json(self):
        return {
            'id': self.id,
            'username': self.username,
            'isActive': self.isActive,
            'isAdmin': self.isAdmin,
            'state_id': self.state_id
        }
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def update_db(self):
        db.session.commit()

    def set_password(self, password):
        self.password = pbkdf2_sha256.hash(password)
    
    def check_password(self, password):
        return pbkdf2_sha256.verify(password, self.password)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def get_all(cls):
        results = db.session.query(
            cls.id, 
            cls.username,
            cls.isActive,
            State.short_name
        ).join(
            State, State.id==cls.state_id
        ).all()
        
        if results:
            json_data = [{
                'id': item.id,
                'username': item.username,
                'isActive': item.isActive,
                'state_name': item.short_name
            } for item in results]
            return json_data
        return None
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter(cls.id==id).first()
    