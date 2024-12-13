from datetime import datetime
from zoneinfo import ZoneInfo
from iJal.app.db import db
from iJal.app.models.livestocks import Livestock


class BlockLivestock(db.Model):
    def get_current_time():
        return datetime.now(ZoneInfo('Asia/Kolkata'))
    
    __tablename__ = "block_livestocks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    livestock_id = db.Column(db.ForeignKey('livestocks.id'), nullable=False)
    count = db.Column(db.Integer, nullable=False)
    bt_id = db.Column(db.ForeignKey('block_territory.id'), nullable=False)
    is_approved = db.Column(db.Boolean, nullable=False, default=False)
    created_on = db.Column(db.DateTime, default=get_current_time)
    created_by = db.Column(db.ForeignKey('users.id'), nullable=False)
    
    users = db.relationship('User', backref=db.backref('block_livestocks', lazy='dynamic'))
    livestocks = db.relationship('Livestock', backref=db.backref('block_livestocks', lazy='dynamic'))
    block_territory = db.relationship('BlockTerritory', backref=db.backref('block_livestocks', lazy='dynamic'))

    def __init__(self,livestock_id,count,bt_id,is_approved,created_by):
        self.livestock_id = livestock_id
        self.count = count
        self.bt_id = bt_id
        self.is_approved = is_approved
        self.created_by = created_by
        
    def json(self):
        return {
            "id":self.id,
            "livestock_id":self.livestock_id,
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
            cls.livestock_id, 
            cls.count,
            cls.is_approved,
            Livestock.livestock_name,
        ).join(Livestock, Livestock.id==cls.livestock_id
        ).filter(cls.bt_id==bt_id)

        results = query.all()

        if results:
            json_data = [{'id': item.id, 
                          'livestock_id':item.livestock_id, 
                          'count': item.count, 
                          'is_approved': item.is_approved,
                          'livestock_name':item.livestock_name} for item in results]
            return json_data
        else:
            return None
        
    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter(cls.id==id).first()

    def update_db(self):
        # db.session.add(self)
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()