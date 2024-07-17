from sqlalchemy import func
from iWater.app.db import db
from iWater.app.models.livestocks import Livestock
from iWater.app.models.village import Village

class LivestockCensus(db.Model):
    __tablename__ = 'livestock_census'
    __table_args__ = (
        db.UniqueConstraint('livestock_id', 'village_id'),
    )

    id = db.Column(db.Integer, primary_key=True, server_default=db.text("nextval('livestock_census_id_seq'::regclass)"))
    livestock_number = db.Column(db.Integer)
    livestock_id = db.Column(db.ForeignKey('livestocks.id'), nullable=False)
    village_id = db.Column(db.ForeignKey('villages.id'), nullable=False)

    livestock = db.relationship('Livestock')
    village = db.relationship('Village')

    def __init__(self,livestock_number,livestock_id,village_id):
        self.livestock_number = livestock_number
        self.livestock_id = livestock_id
        self.village_id = village_id
    
    def json(self):
        return {
            'id': self.id,
            'livestock_id': self.livestock_id,
            'livestock_number': self.livestock_number,
            'village_id' : self.village_id
        }
    
    
    @classmethod
    def get_by_village_id(cls, village_ids):
        query = db.session.query(
        Livestock.type,
        Livestock.name,
        func.sum(cls.livestock_number).label('livestock_number'),
        func.avg(Livestock.water_use).label('water_use')
        ).join(Livestock, Livestock.id == cls.livestock_id)\
        .filter(cls.village_id.in_(village_ids))\
        .group_by(Livestock.id, Livestock.name, Livestock.type).all()
        return query
        
    @classmethod
    def get_livestock_census(cls, json_data):
        query = db.session.query(
        Livestock.type,
        Livestock.name,
        func.sum(cls.livestock_number).label('livestock_number'),
        func.avg(Livestock.water_use).label('water_use')
        ).join(Livestock, Livestock.id == cls.livestock_id)\
        .join(Village, Village.id == cls.village_id)\
        

        if 'village_id' in json_data:
            query = query.filter(cls.village_id== json_data['village_id'])\
            .group_by(Livestock.id, Livestock.name, Livestock.type)
        elif 'block_id' in json_data:
            query = query.filter(Village.block_id == json_data['block_id'])\
            .group_by(Livestock.id, Livestock.name, Livestock.type)
        elif 'district_id' in json_data:
            query = query.filter(Village.district_id == json_data['district_id'])\
            .group_by(Livestock.id, Livestock.name, Livestock.type)
        
        result = query.all()
        return query
    
    @classmethod
    def get_existing_data(cls, json_data,_livestock_id):
        # query = db.session.query(filter(cls.livestock_id ==_livestock_id))
        query=cls.query.filter_by(livestock_id=_livestock_id)

        if 'village_id' in json_data:
            query = query.filter(cls.village_id== json_data['village_id'])
        elif 'block_id' in json_data:
            query = query.filter(Village.block_id == json_data['block_id'])
        elif 'district_id' in json_data:
            query = query.filter(Village.district_id == json_data['district_id'])
        
        result = query.first()
        if result:
            return result.json()
        else:
            return None
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(_id):
        participant = LivestockCensus.query.filter_by(id=_id).first()
        db.session.delete(participant)
        db.session.commit()

    def commit_db():
        db.session.commit()

    def update_db(data,_id):
        user = LivestockCensus.query.filter_by(id=_id).update(data)
        db.session.commit()