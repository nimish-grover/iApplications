from zoneinfo import ZoneInfo
from iJal.app.db import db
from datetime import datetime

from iJal.app.models.waterbody import WaterbodyType

class BlockWaterbody(db.Model):
    def get_current_time():
        return datetime.now(ZoneInfo('Asia/Kolkata'))
    
    __tablename__ = 'block_waterbodies'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    count = db.Column(db.Integer, nullable=False)
    area = db.Column(db.Float, nullable=False)
    storage = db.Column(db.Float, nullable=False)
    is_approved = db.Column(db.Boolean, nullable=False, default=False)
    created_on = db.Column(db.DateTime, default=get_current_time)
    wb_type_id = db.Column(db.ForeignKey('waterbody_types.id'), nullable=False)
    bt_id = db.Column(db.ForeignKey('block_territory.id'), nullable=False)
    created_by = db.Column(db.ForeignKey('users.id'), nullable=False)
    
    users = db.relationship('User', backref=db.backref('block_waterbodies', lazy='dynamic'))
    waterbodies = db.relationship('WaterbodyType', backref=db.backref('block_waterbodies', lazy='dynamic'))
    block_territory = db.relationship('BlockTerritory', backref=db.backref('block_waterbodies', lazy='dynamic'))
    
    
    def __init__(self, wb_type_id, count, storage, bt_id, is_approved, created_by):
        self.wb_type_id = wb_type_id
        self.count = count
        self.area = 0
        self.storage = storage
        self.bt_id = bt_id
        self.is_approved = is_approved
        self.created_by = created_by
        
    def json(self):
        return {
            "id":self.id,
            "wb_type_id":self.wb_type_id,
            "area":self.area,
            "storage":self.storage,
            "count":self.count,
            "bt_id":self.bt_id,
            "is_approved":self.is_approved,
            "created_by":self.created_by,
            "creatd_on":self.created_on
        }
    
    @classmethod
    def get_by_bt_id(cls, bt_id):
        query = db.session.query(
            cls.id, 
            cls.storage,
            cls.count,
            cls.is_approved,
            cls.bt_id,
            WaterbodyType.waterbody_name
        ).join(WaterbodyType, WaterbodyType.id==cls.wb_type_id
        ).filter(cls.bt_id == bt_id)
        
        results = query.all()

        if results:
            json_data = [{'id':item.id, 
                          'storage':item.storage, 
                          'count':item.count, 
                          'is_approved':item.is_approved,
                          'bt_id':item.bt_id,
                          'waterbody_name':item.waterbody_name} 
                          for item in results]
            return json_data
        else:
            return None
        
    @classmethod  
    def get_by_id(cls, id):
        return cls.query.filter(cls.id==id).first()
    
    def update_db(self):
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(object):
        db.session.delete(object)
        db.session.commit()