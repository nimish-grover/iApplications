from flask_login import UserMixin
from iJalagam.app.db import db
from passlib.hash import pbkdf2_sha256

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(300))
    isActive = db.Column(db.Boolean, nullable=False, default=False)
    isAdmin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, username, password, isActive, isAdmin):
        self.username = username
        self.password = password
        self.isActive = isActive
        self.isAdmin = isAdmin

    def json(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'isActive': self.isActive,
            'isAdmin': self.isAdmin
        }
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def set_password(self, password):
        self.password = pbkdf2_sha256.hash(password)
    
    def check_password(self, password):
        return pbkdf2_sha256.verify(password, self.password)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()