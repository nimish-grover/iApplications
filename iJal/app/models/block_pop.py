from datetime import datetime
from zoneinfo import ZoneInfo
from iJal.app.db import db
from iJal.app.models.population import Population


class BlockPop(db.Model):
    def get_current_time():
        return datetime.now(ZoneInfo("Asia/Kolkata"))
    
    __tablename__ = "block_pops"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    count = db.Column(db.Integer, nullable=False)
    created_on = db.Column(db.DateTime, default=get_current_time)
    bt_id = db.Column(db.Integer, db.ForeignKey('block_territory.id'), nullable=False)
    population_id = db.Column(db.Integer, db.ForeignKey('population.id'), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_approved = db.Column(db.Boolean, nullable=False, default=False)

    block_territory = db.relationship('BlockTerritory', backref=db.backref('block_pops', lazy='dynamic'))
    population = db.relationship('Population', backref=db.backref('block_pops', lazy='dynamic'))
    user = db.relationship('User', backref=db.backref('block_pops', lazy='dynamic'))

    def __init__(self,population_id,count,bt_id,is_approved,created_by):
        self.population_id = population_id
        self.count = count
        self.bt_id = bt_id
        self.created_by = created_by
        self.is_approved = is_approved
        
    def json(self):
        return {
            "id":self.id,
            "population_id":self.population_id,
            "count":self.count,
            "bt_id":self.bt_id,
            "is_approved": self.is_approved,
            "created_by":self.created_by,
            "creatd_on":self.created_on
        }
    
    @classmethod
    def get_by_bt_id(cls, bt_id):
        query =  db.session.query(
            cls.id,
            cls.population_id, 
            cls.count.label('count'),
            Population.population_type.label('category'),
            Population.display_name,
            cls.is_approved
        ).join(Population, Population.id==cls.population_id).filter(cls.bt_id==bt_id)

        results = query.all()

        if results:
            json_data = [{'id': item.id, 'population_id':item.population_id, 'count': item.count, 'category': item.category, 'display_name':item.display_name, 'is_approved':item.is_approved} for item in results]
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