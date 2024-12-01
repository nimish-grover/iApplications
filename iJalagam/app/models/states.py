import json

from sqlalchemy import DefaultClause
from iJalagam.app.db import db
from iJalagam.app.models.districts import District


class State(db.Model):
    __tablename__ = 'states'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    code = db.Column(db.Integer, nullable=False, unique=True)
    census_code = db.Column(db.Integer, default=0)
    local_name = db.Column(db.String(100))
    is_state = db.Column(db.Boolean, default=False)

    def __init__(self, name, code, census_code, local_name, is_state):
        self.name = name
        self.code = code
        self.census_code = census_code
        self.local_name = local_name
        self.is_state = is_state 

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'census_code':self.census_code,
            'local_name': self.local_name,
            'is_state': self.is_state
        }

    @classmethod
    def get_states(cls):
        return cls.query.order_by(cls.name).all()
    

    @classmethod
    def get_breadcrumps(cls, json_data):
        from app.models import Block, District, Village 
        query = db.session.query(State.name.label('state'), 
                                 District.name.label('district'), 
                                 Block.name.label('block'), 
                                 Village.name.label('village'))\
                    .join(District, State.id == District.state_id)\
                    .join(Block, District.id == Block.district_id)\
                    .join(Village, Block.id == Village.block_id)
    
        if 'village_id' in json_data:
                query = db.session.query(State.name.label('state'), 
                                 District.name.label('district'), 
                                 Block.name.label('block'), 
                                 Village.name.label('village'))\
                    .join(District, State.id == District.state_id)\
                    .join(Block, District.id == Block.district_id)\
                    .join(Village, Block.id == Village.block_id)\
                    .filter(Village.id == json_data['village_id'])
        elif 'block_id' in json_data:
            query = db.session.query(State.name.label('state'), 
                                 District.name.label('district'), 
                                 Block.name.label('block'))\
                    .join(District, State.id == District.state_id)\
                    .join(Block, District.id == Block.district_id)\
                    .filter(Block.id == json_data['block_id'])
        elif 'district_id' in json_data:
            query = db.session.query(State.name.label('state'), 
                                 District.name.label('district'))\
                    .join(District, State.id == District.state_id)\
                    .filter(District.id == json_data['district_id'])
            
        result = query.first()
        return result
    
    @classmethod
    def get_aspirational_states(cls):
        results = cls.query.join(District, District.state_id==cls.id
                                ).filter(District.code.in_([745,196,641,72,20,338,563,9,434,398,431,426,405,500,92,115,112,227,583,596,610,721,129,119,132])
                                ).order_by(cls.name).all()
        if results:
            # json_data = [result.json for result in results]
            return results
        else:
            return None