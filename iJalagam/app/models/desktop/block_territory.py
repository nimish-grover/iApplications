from sqlalchemy import and_, func
from iJalagam.app import db
from datetime import datetime,timezone


class BlockTerritory(db.Model):
    __tablename__ = 'block_territory'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    state_id = db.Column(db.ForeignKey('states.id'), nullable=False)
    district_id = db.Column(db.ForeignKey('districts.id'), nullable=False)
    block_id = db.Column(db.ForeignKey('blocks.id'), nullable=False)
    isApproved = db.Column(db.Boolean, default=True)
    created_on = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    states = db.relationship('State')
    districts = db.relationship('District')
    blocks = db.relationship('Block')
    
    def __init__(self,state_id,district_id,block_id,isApproved=True):
        self.state_id = state_id
        self.district_id = district_id
        self.block_id = block_id
        self.isApproved = isApproved

        
    def json(self):
        return {
            "id":self.id,
            "state_id":self.state_id,
            "district_id":self.district_id,
            "block_id":self.block_id,
            "isApproved":self.isApproved,
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