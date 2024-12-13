from sqlalchemy import and_, func
from iJalagam.app import db
from datetime import datetime,timezone


class BlockWaterbody(db.Model):
    __tablename__ = 'block_waterbodies'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    wb_type_id = db.Column(db.ForeignKey('waterbody_types.id'), nullable=False)
    count = db.Column(db.Integer, nullable=False)
    storage = db.Column(db.Float, nullable=False)
    b_territory_id = db.Column(db.ForeignKey('block_territory.id'), nullable=False)
    isApproved = db.Column(db.Boolean, nullable=False, default=False)
    created_on = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    created_by = db.Column(db.ForeignKey('users.id'), nullable=False)
    
    users = db.relationship('User')
    waterbodies = db.relationship('WaterbodyType')
    block_territory = db.relationship('BlockTerritory')
    
    
    def __init__(self,wb_type_id,count,storage,b_territory_id,isApproved,created_by):
        self.wb_type_id = wb_type_id
        self.count = count
        self.storage = storage
        self.b_territory_id = b_territory_id
        self.isApproved = isApproved
        self.created_by = created_by
        
    def json(self):
        return {
            "id":self.id,
            "wb_type_id":self.wb_type_id,
            "storage":self.storage,
            "count":self.count,
            "b_territory_id":self.b_territory_id,
            "isApproved":self.isApproved,
            "created_by":self.created_by,
            "creatd_on":self.created_on
        }
    

    @classmethod
    def get_by_territory_id(cls,_territory_id):
        query = cls.query.filter_by(b_territory_id=_territory_id).all()
        if query:
            json_data = [result.json() for result in query]
            return json_data
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

    @classmethod
    def save_multiple_to_db(cls,array):
        db.session.add_all(array)
        db.session.commit()
        
    @classmethod
    def update_multiple(cls,data):
        db.session.bulk_update_mappings(cls, data)
        db.session.commit()