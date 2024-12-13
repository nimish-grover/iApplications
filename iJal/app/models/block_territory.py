from zoneinfo import ZoneInfo
from sqlalchemy import and_, func
from iJal.app.db import db
from datetime import datetime, timezone


class BlockTerritory(db.Model):
    __tablename__ = 'block_territory'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    state_id = db.Column(db.ForeignKey('states.id'), nullable=False)
    district_id = db.Column(db.ForeignKey('districts.id'), nullable=False)
    block_id = db.Column(db.ForeignKey('blocks.id'), unique=True, nullable=False)
    is_approved = db.Column(db.Boolean, nullable=False, default=False)
    created_on = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(ZoneInfo('Asia/Kolkata')))
    
    state = db.relationship('State', backref=db.backref('block_territory', lazy='dynamic'))
    district = db.relationship('District', backref=db.backref('block_territory', lazy='dynamic'))
    block = db.relationship('Block', backref=db.backref('block_territory', lazy='dynamic'))
    
    def __init__(self,state_id,district_id, block_id, is_approved=False):
        self.state_id = state_id
        self.district_id = district_id
        self.block_id = block_id
        self.is_approved = is_approved

        
    def json(self):
        return {
            "id":self.id,
            "state_id":self.state_id,
            "district_id":self.district_id,
            "block_id":self.block_id,
            "is_approved":self.is_approved,
            "created_on":self.created_on
        }
    
    
    @classmethod
    def get_by_block_id(cls,_block_id):
        query = cls.query.filter_by(block_id=_block_id).first()
        if query:
            return query.json()
        else:
            return None
    
    @classmethod
    def get_bt_id(cls, block_id, district_id, state_id):
        return cls.query.with_entities(cls.id).filter(block_id==block_id, district_id==district_id, state_id==state_id).scalar()
    
    @classmethod
    def get_all(cls):
        query=cls.query.order_by(cls.id.desc())
        return query

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def delete_from_db(cls,_id):
        user = cls.query.filter_by(id=_id).first()
        db.session.delete(user)
        db.session.commit()

    def commit_db():
        db.session.commit()

    @classmethod
    def update_db(cls,data,_id):
        user = cls.query.filter_by(id=_id).update(data)
        db.session.commit()