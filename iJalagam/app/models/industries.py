from datetime import datetime

from sqlalchemy import func
from iJalagam.app import db


class Industry(db.Model):
    __tablename__ = "industries"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(),nullable=False)
    short_name = db.Column(db.String(100), nullable=False) # sc, st, male, female
    display_name = db.Column(db.String(100), nullable=False)

    

    def __init__(self, name,short_name,display_name):
        self.name = name
        self.display_name = display_name
        self.short_name = short_name


    def json(self):
        return {
            'id':self.id,
            'name': self.name,
            'display_name':self.display_name,
            'short_name':self.short_name
        }
    
    @classmethod
    def get_all(cls):
        query = cls.query.order_by(cls.id).all()
        json_data = [result.json() for result in query]
        if json_data:
            return json_data
        else:
            return None

    def update_to_db():
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        # db.session.commit()