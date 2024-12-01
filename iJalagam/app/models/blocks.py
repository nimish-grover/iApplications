from sqlalchemy import and_, null
from iJalagam.app.db import db
from iJalagam.app.models import District, State

class Block(db.Model):
    __tablename__ = 'blocks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.Integer, nullable=False)
    census_code = db.Column(db.Integer)
    district_id = db.Column(db.ForeignKey('districts.id'), nullable=False)
    state_id = db.Column(db.ForeignKey('states.id'), nullable=False)
    local_name = db.Column(db.String(100))

    district = db.relationship('District')
    state = db.relationship('State')

    def __init__(self, name, code, census_code, district_id, state_id, local_name):
        self.name = name
        self.code = code
        self.census_code = census_code
        self.district_id = district_id
        self.state_id = state_id
        self.local_name = local_name


    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'census_code': self.census_code,
            'district_id': self.district_id,
            'state_id': self.state_id,
            'local_name': self.local_name
        }


    @classmethod
    def get_blocks(cls, district_id):
        results = cls.query.filter_by(district_id = district_id).order_by(cls.name).all()
        if results:
            json_data = [result.json() for result in results]
            return json_data
        else:
            return None
    
    @classmethod
    def get_district_by_block(cls, block_id):
        return cls.query.filter_by(id = block_id).first()
    
    @classmethod
    def get_id_and_name(cls, block_id, district_id, state_id):
        query = db.session.query(
            cls.id.label('block_id'),
            cls.name.label('block_name'),
            District.id.label('district_id'),
            District.name.label('district_name'),
            State.id.label('state_id'),
            State.name.label('state_name'),
        ).join(District, District.id == cls.district_id
        ).join(State, State.id == District.state_id
        ).filter(and_(Block.id == block_id, District.id==district_id)
        ).order_by(cls.name)

        result = query.first()

        if result:
            json_data = {'block':{'id':result[0], 'name': result[1]},
                         'district':{'id':result[2], 'name': result[3]},
                         'state':{'id':result[4], 'name': result[5]},}
            return json_data
        else:
            return None
        
    @classmethod
    def get_aspirational_blocks(cls, district_id):
        results = cls.query.filter(cls.code.in_([4876,6653,7130,539,172,3209,6050,7047,4027,3784,4010,3979,3837,4628,624,781,762,2157,6287,6468,6255,5250,951,823,994]), 
                                   cls.district_id==district_id).order_by(cls.name).all()
        if results:
            json_data = [result.json() for result in results]
            return json_data
        else:
            return None 
        # from iJalagam.app.models.groundwater_extraction import GroundwaterExtraction
        # results = db.session.query(
        #     cls.id.label('block_id'),
        #     cls.name.label('block_name'),
        #     District.id.label('district_id'),
        #     District.name.label('district_name'),
        #     State.id.label('state_id'),
        #     State.name.label('state_name'),
        #     GroundwaterExtraction.category.label('category')
        # ).join(District, District.id == cls.district_id
        # ).join(State, State.id == District.state_id
        # ).outerjoin(GroundwaterExtraction, GroundwaterExtraction.block_id==cls.id
        # ).filter(cls.code.in_([4876,6653,7130,539,172,3209,6050,7047,4027,3784,4010,3979,3837,4628,624,781,762,2157,6287,6468,6255,5250,951,823,994]),
        #          District.code.in_([745,196,641,72,20,338,563,9,434,398,431,426,405,500,92,115,112,227,583,596,610,721,129,119,132]) 
        # ).order_by(cls.name).all()
        # def replace_semi_critical(category):
        #     if category:
        #         if category.lower() == 'semi_critical':
        #             return 'critical'
        #     else:
        #         return 'na'
        #     return category
        # if results:
        #     return [{
        #         'block_id':item[0],
        #         'block_name':item[1],
        #         'district_id':item[2],
        #         'district_name':item[3],
        #         'state_id':item[4],
        #         'state_name':item[5],
        #         'category':replace_semi_critical(item[6])
        #     } for item in results]
        # else:
        #     return None
        # return cls.query.filter_by(id.contains(4876,6653,7130,539,172,3209,6050,7047,4027,3784,4010,3979,3837,4628,624,781,762,2157,6287,6468,6255,5250,951,823,994)).all()