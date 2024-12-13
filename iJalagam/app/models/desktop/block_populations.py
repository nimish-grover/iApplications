from sqlalchemy import and_, func
from iJalagam.app import db
from datetime import datetime
from pytz import timezone



ist = timezone("Asia/Kolkata")

class BlockPopulation(db.Model):
    __tablename__ = 'block_populations'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    population_id = db.Column(db.ForeignKey('population.id'), nullable=False)
    count = db.Column(db.Integer, nullable=False)
    b_territory_id = db.Column(db.ForeignKey('block_territory.id'), nullable=False)
    created_on = db.Column(db.DateTime, default=lambda: datetime.now(ist))
    created_by = db.Column(db.ForeignKey('users.id'), nullable=False)
    isApproved = db.Column(db.Boolean,default=False)
    
    users = db.relationship('User')
    populations = db.relationship('Population')
    block_territory = db.relationship('BlockTerritory')

    
    def __init__(self,population_id,count,b_territory_id,isApproved,created_by):
        self.population_id = population_id
        self.count = count
        self.b_territory_id = b_territory_id
        self.created_by = created_by
        self.isApproved = isApproved
        
    def json(self):
        return {
            "id":self.id,
            "population_id":self.population_id,
            "count":self.count,
            "b_territory_id":self.b_territory_id,
            "isApproved": self.isApproved,
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
    def get_id(cls,_territory_id,_population_id):
        query = cls.query.filter(b_territory_id=_territory_id,population_id=_population_id).scalar()
        if not query:
            return None
        return query    
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