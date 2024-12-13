from datetime import datetime
from zoneinfo import ZoneInfo
from iJal.app.db import db


class BlockIndustry(db.Model):
    def get_current_time():
        return datetime.now(ZoneInfo('Asia/Kolkata'))
    
    __tablename__ = 'block_industries'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    industry_id = db.Column(db.Integer, db.ForeignKey('industries.id'), nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    allocation = db.Column(db.Float, nullable=False)
    bt_id = db.Column(db.Integer, db.ForeignKey('block_territory.id'), nullable=False)
    is_approved = db.Column(db.Boolean, nullable=False, default=False)
    created_on = db.Column(db.DateTime, default=get_current_time)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    users = db.relationship('User', backref=db.backref('block_industries', lazy='dynamic'))
    block_territory = db.relationship('BlockTerritory', backref=db.backref('block_industries', lazy='dynamic'))
    industries = db.relationship('Industry', backref=db.backref('block_industries', lazy='dynamic'))
    
    def __init__(self,industry_id,allocation,unit,bt_id,is_approved,created_by):
        self.industry_id = industry_id
        self.allocation = allocation
        self.unit = unit
        self.bt_id = bt_id
        self.is_approved = is_approved
        self.created_by = created_by
        
    def json(self):
        return {
            "id":self.id,
            "industry_id":self.industry_id,
            "unit":self.unit,
            "allocation":self.allocation,
            "is_approved":self.is_approved,
            "bt_id":self.bt_id,
            "created_by":self.created_by,
            "creatd_on":self.created_on
        }
    
    @classmethod
    def get_industries():
        pass