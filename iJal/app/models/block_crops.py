from datetime import datetime
from zoneinfo import ZoneInfo
from iJal.app.db import db
from iJal.app.models.crops import Crop

class BlockCrop(db.Model):
    def get_current_time():
        return datetime.now(ZoneInfo('Asia/Kolkata'))
    
    __tablename__ = 'block_crops'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    crop_id = db.Column(db.ForeignKey('crops.id'), nullable=False)
    area = db.Column(db.Float, nullable=False)
    bt_id = db.Column(db.ForeignKey('block_territory.id'), nullable=False)
    created_on = db.Column(db.DateTime, default=get_current_time)
    created_by = db.Column(db.ForeignKey('users.id'), nullable=False)
    is_approved = db.Column(db.Boolean, nullable=False, default=False)
    
    users = db.relationship('User', backref=db.backref('block_crops', lazy='dynamic'))
    block_territory = db.relationship('BlockTerritory', backref=db.backref('block_crops', lazy='dynamic'))
    crops = db.relationship('Crop', backref=db.backref('block_crops', lazy='dynamic'))
    
    def __init__(self,crop_id,area,bt_id,created_by,is_approved):
        self.crop_id = crop_id
        self.area = area
        self.bt_id = bt_id
        self.is_approved = is_approved
        self.created_by = created_by
        
    def json(self):
        return {
            "id":self.id,
            "crop_id":self.crop_id,
            "area":self.area,
            "bt_id":self.bt_id,
            "isAprroved":self.is_approved,
            "created_by":self.created_by,
            "creatd_on":self.created_on
        }
    
    @classmethod
    def get_by_bt_id(cls, bt_id):
        query = db.session.query(
            cls.id, 
            cls.crop_id, 
            cls.area.label('crop_area'),
            cls.is_approved,
            Crop.crop_name
        ).join(Crop, Crop.id==cls.crop_id
        ).filter(cls.bt_id==bt_id)

        results = query.all()

        if results:
            json_data = [{
                'id': item.id,
                'crop_id': item.crop_id,
                'crop_area': item.crop_area,
                'crop_name': item.crop_name,
                'is_approved': item.is_approved
                } for item in results]
            return json_data        
        else:
            return None
        
    @classmethod    
    def get_by_id(cls, id):
        return cls.query.filter(cls.id==id).first()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update_db(self):
        db.session.commit()
    