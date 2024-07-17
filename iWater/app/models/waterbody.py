from sqlalchemy import case, func
from iWater.app.db import db
from iWater.app.models.village import Village
from iWater.app.models.state import State
from iWater.app.models.district import District
from iWater.app.models.block import Block
from iWater.app.models.village import Village

class Waterbody(db.Model):
    __tablename__ = 'waterbodies'

    id = db.Column(db.Integer, primary_key=True, server_default=db.text("nextval('waterbodies_id_seq'::regclass)"))
    waterbody_area = db.Column(db.Float(53), nullable=False)
    village_id = db.Column(db.ForeignKey('villages.id'), nullable=False)

    village = db.relationship('Village')

    @classmethod
    def get_waterbodies(cls, json_data):
        query = db.session.query(
            cls.waterbody_area.label('area'),
            case(
                    (cls.waterbody_area < 10, 'small'),
                    (cls.waterbody_area > 100, 'large'),
                else_='medium'
            ).label('waterbody')
        ).join(Village, Village.id == cls.village_id)
        
        if 'village_id' in json_data:
            query = query.filter(cls.village_id == json_data['village_id'])
        if 'block_id' in json_data:            
            query = query.filter(Village.block_id == json_data['block_id'])\
                    # .group_by('waterbody')
        elif 'district_id' in json_data:
            query = query.filter(Village.district_id == json_data['district_id'])\
                    # .group_by('waterbody')
        
        result = query.all()
        return result
    
    # @classmethod
    # def get_total_crop_types(cls):
    #     query = db.session.query(
    #     func.count(db.distinct(Crops_type.type))). \
    #     join(Village, cls.village_code == Village.code).\
    #     join(Block, Village.block_id == Block.id).\
    #     join(District, cls.district_code == District.code).\
    #     join(State, District.state_id == State.id)