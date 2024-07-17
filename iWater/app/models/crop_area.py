from iWater.app.db import db
from iWater.app.models import State
from iWater.app.models import District
from iWater.app.models import Block
from iWater.app.models import Village
from iWater.app.models.crops_type import Crops_type
from iWater.app.models.crops import Crops
from sqlalchemy import func

class Crop_area(db.Model):
    __tablename__ = 'crop_area'

    id = db.Column(db.Integer, primary_key= True)
    district_code=db.Column(db.Integer,nullable=False)
    village_code=db.Column(db.Integer,nullable=False)
    crop_id=db.Column(db.Integer,nullable=False)
    crop_type_id=db.Column(db.Integer,nullable=False)
    crop_area = db.Column(db.Float,nullable=False)

    
    def __init__(self,district_code,village_code,crop_id,crop_type_id,crop_area):
        self.crop_area = crop_area
        self.district_code = district_code
        self.village_code = village_code
        self.crop_id = crop_id
        self.crop_type_id = crop_type_id

    
    def json(self):
        return {
            'id': self.id,
            'crop_type_id': self.crop_type_id,
            'crop_area': self.crop_area,
            'district_code' : self.district_code,
            'village_code' : self.village_code,
            'crop_id' : self.crop_id,
        }
    
    @classmethod
    def get_wb_by_id(cls, _id):
        query=cls.query.filter_by(id=_id).first()
        if query:
            return query.json()
        else:
            return None
    
    @classmethod
    def get_wb_by_type_id(cls, _type_id):
        query =  cls.query.filter_by(type_id=_type_id).first()
        if query:
            return query.json()
        else:
            return None
    
    @classmethod
    def get_all(cls):
        query=cls.query.order_by(cls.name)
        return query

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(_id):
        participant = Crop_area.query.filter_by(id=_id).first()
        db.session.delete(participant)
        db.session.commit()

    def commit_db():
        db.session.commit()

    def update_db(data,_id):
        user = Crop_area.query.filter_by(id=_id).update(data)
        db.session.commit()
        
    @classmethod
    def get_crop_area(cls,json_data):
        query = db.session.query(
        Crops_type.type,
        Crops.name,
        Crop_area.crop_area,
        Crops.water_required_per_hectare,
        Crops_type.id). \
        join(Crop_area, Crop_area.crop_type_id == Crops_type.id).\
        join(Crops, Crops.id == Crop_area.crop_id).\
        join(Village, Crop_area.village_code == Village.code).\
        join(Block, Village.block_id == Block.id).\
        join(District, Crop_area.district_code == District.code).\
        join(State, District.state_id == State.id)
        
        
        if 'state_id' in json_data:
            query = query.filter(State.code == json_data['state_id']).all()
        
        elif 'village_id' in json_data:
            query = query.filter(Village.code == json_data['village_id']).all()
            
        elif 'district_id' in json_data:
            query = query.filter(District.code == json_data['district_id']).all()
        
        elif 'block_id' in json_data:
            query = query.filter(Block.code == json_data['block_id']).all()
        else:
            query = query.all()
        return query
    """
    SELECT crops_type.type, crops.name,crop_area.crop_area, crops.water_required_per_hectare FROM crop_area 
    INNER join crops on crops.id = crop_area.crop_id 
    inner join crops_type on crop_area.crop_type_id = crops_type.id LIMIT 100
    """
    
    @classmethod
    def get_total_crop_types(cls,json_data):
        query = db.session.query(
        func.count(db.distinct(Crops_type.type))). \
        join(Crop_area, Crop_area.crop_type_id == Crops_type.id).\
        join(Crops, Crops.id == Crop_area.crop_id).\
        join(Village, Crop_area.village_code == Village.code).\
        join(Block, Village.block_id == Block.id).\
        join(District, Crop_area.district_code == District.code).\
        join(State, District.state_id == State.id)
        
        
        if 'state_code' in json_data:
            query = query.filter(State.code == json_data['state_code']).scalar()
        
        elif 'village_code' in json_data:
            query = query.filter(Village.code == json_data['village_code']).scalar()
            
        elif 'district_code' in json_data:
            query = query.filter(District.code == json_data['district_code']).scalar()
        
        elif 'block_code' in json_data:
            query = query.filter(Block.code == json_data['block_code']).scalar()
        else:
            query = query.scalar()
        return query
    
    @classmethod
    def get_existing_data(cls, json_data):
        # query = db.session.query(filter(cls.livestock_id ==_livestock_id))
        query=cls.query.filter_by(crop_id= json_data['crop_id'],crop_type_id = json_data['crop_type_id'], district_code = json_data['district_id'])

        if 'village_id' in json_data:
            query = query.filter(cls.village_code== json_data['village_id'])

        
        result = query.first()
        if result:
            return result.json()
        else:
            return None