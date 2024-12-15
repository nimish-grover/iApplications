from datetime import datetime
from zoneinfo import ZoneInfo
from iJal.app.db import db
from iJal.app.models.lulc import LULC


class BlockLULC(db.Model):
    def get_current_time():
        return datetime.now(ZoneInfo('Asia/Kolkata'))
    
    __tablename__ = 'block_lulc'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    area = db.Column(db.Float, nullable=False)
    bt_id = db.Column(db.ForeignKey('block_territory.id'), nullable=False)
    is_approved = db.Column(db.Boolean, nullable=False, default=False)
    created_on = db.Column(db.DateTime, default=get_current_time)
    lulc_id = db.Column(db.ForeignKey('lulc.id'), nullable=False)
    created_by = db.Column(db.ForeignKey('users.id'), nullable=False)
    
    users = db.relationship('User', backref=db.backref('block_lulc', lazy='dynamic'))
    lulc = db.relationship('LULC', backref=db.backref('block_lulc', lazy='dynamic'))
    block_territory = db.relationship('BlockTerritory', backref=db.backref('block_lulc', lazy='dynamic'))

    
    def __init__(self,lulc_id,area,bt_id,is_approved,created_by):
        self.lulc_id = lulc_id
        self.area = area
        self.bt_id = bt_id
        self.is_approved = is_approved
        self.created_by = created_by
        
    def json(self):
        return {
            "id":self.id,
            "area":self.area,
            "lulc_id":self.lulc_id,
            "bt_id":self.bt_id,
            "is_approved":self.is_approved,
            "created_by":self.created_by,
            "creatd_on":self.created_on
        }
    
    @classmethod    
    def get_by_id(cls, id):
        return cls.query.filter(cls.id==id).first()

    @classmethod
    def get_by_bt_id(cls, bt_id):
        query = db.session.query(
            cls.id, 
            cls.area,
            cls.lulc_id,
            LULC.display_name,
            cls.bt_id,
            cls.is_approved
        ).join(
            LULC,LULC.id==cls.lulc_id
        ).filter(
            cls.bt_id == bt_id
        )

        results = query.all()
        if results:
            json_data = [{
                'id': row.id,
                'area': row.area,
                'lulc_id': row.lulc_id,
                'lulc_name':row.display_name,
                'bt_id': row.bt_id,
                'is_approved': row.is_approved
                } for row in results]
            return json_data

        return None
    
    @classmethod
    def get_all(cls):
        query=cls.query.order_by(cls.id.desc())
        return query

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update_db(self):
        db.session.commit()
        
    def delete_from_db(object):
        db.session.delete(object)
        db.session.commit()