from sqlalchemy import and_, func
from iJalagam.app import db
from sqlalchemy.orm import load_only


class CensusData(db.Model):
    __tablename__ = 'census_data'

    id = db.Column(db.Integer, primary_key=True)
    tga = db.Column(db.Float)
    households = db.Column(db.Integer, nullable=False)
    male_population = db.Column(db.Integer)
    female_population = db.Column(db.Integer)
    sc_male_population = db.Column(db.Integer)
    sc_female_population = db.Column(db.Integer)
    st_male_population = db.Column(db.Integer)
    st_female_population = db.Column(db.Integer)
    forest_area = db.Column(db.Float)
    non_agriculture_area = db.Column(db.Float)
    uncultivable_area = db.Column(db.Float)
    grazing_area = db.Column(db.Float)
    misc_area = db.Column(db.Float)
    wasteland_area = db.Column(db.Float)
    fallow_area = db.Column(db.Float)
    current_fallow_area = db.Column(db.Float)
    # net_sown_area = db.Column(db.Integer) = unirrigated + irrigated
    unirrigated_area = db.Column(db.Float)
    # irrigated_area = db.Column(db.Integer) = canal_area + tubewell_area + tank_area + waterfall_area + other_area !important    
    canal_area = db.Column(db.Float)
    tubewell_area = db.Column(db.Float)
    tank_area = db.Column(db.Float)
    waterfall_area = db.Column(db.Float)
    other_area = db.Column(db.Float)
    village_id = db.Column(db.ForeignKey('villages.id'), nullable=False)
    block_id = db.Column(db.ForeignKey('blocks.id'), nullable=False)
    district_id = db.Column(db.ForeignKey('districts.id'), nullable=False)
    state_id = db.Column(db.ForeignKey('states.id'), nullable=False)
    local_name = db.Column(db.String(100))

    village = db.relationship('Village')
    block = db.relationship('Block')
    district = db.relationship('District')
    state = db.relationship('State')

    def __init__(self, tga,households,male_population,female_population,sc_male_population,sc_female_population, 
                 st_male_population, st_female_population, forest_area, non_agriculture_area, uncultivable_area, grazing_area,
                 misc_area,wasteland_area, fallow_area, current_fallow_area, unirrigated_area, canal_area, tubewell_area,
                 tank_area, waterfall_area, other_area, village_id, block_id, district_id, state_id):
        self.tga=tga
        self.households = households
        self.male_population = male_population
        self.female_population = female_population
        self.sc_male_population = sc_male_population
        self.sc_female_population = sc_female_population
        self.st_male_population =st_male_population
        self.st_female_population = st_female_population
        self.forest_area - forest_area
        self.non_agriculture_area = non_agriculture_area
        self.uncultivable_area = uncultivable_area
        self.grazing_area = grazing_area
        self.misc_area = misc_area
        self.wasteland_area = wasteland_area
        self.fallow_area = fallow_area
        self.current_fallow_area = current_fallow_area
        self.unirrigated_area = unirrigated_area
        self.canal_area = canal_area
        self.tubewell_area = tubewell_area
        self.tank_area = tank_area
        self.waterfall_area = waterfall_area
        self.other_area = other_area
        self.village_id = village_id
        self.block_id = block_id
        self.district_id = district_id
        self.state_id = state_id

    def json(self):
        return {
            'tga' : self.tga,
            'households' : self.households,               
            'male_population' : self.male_population,               
            'female_population' : self.female_population,               
            'sc_male_population' : self.sc_male_population,               
            'sc_female_population' : self.sc_female_population,               
            'st_male_population'    : self.st_male_population,               
            'st_female_population'  : self.st_female_population,               
            'forest_area'           : self.forest_area,               
            'non_agriculture_area'  : self.non_agriculture_area,               
            'uncultivable_area'     : self.uncultivable_area,               
            'grazing_area'          : self.grazing_area,               
            'misc_area'             : self.misc_area,               
            'wasteland_area'        : self.wasteland_area,               
            'fallow_area'           : self.fallow_area,               
            'current_fallow_area'   : self.current_fallow_area,               
            'unirrigated_area'      : self.unirrigated_area,               
            'canal_area'            : self.canal_area,               
            'tubewell_area'         : self.tubewell_area,               
            'tank_area'             : self.tank_area,               
            'waterfall_area'        : self.waterfall_area,               
            'other_area'            : self.other_area,               
            'village_id'            : self.village_id,               
            'block_id'              : self.block_id,               
            'district_id'           : self.district_id,               
            'state_id'              : self.state_id
            }   

    @classmethod
    def get_population_data_by_village(cls, village_id):
        query = cls.query.with_entities(cls.male_population, cls.female_population).filter_by(village_id=village_id)
        results = query.first() 
        if results:
            results = {'male': results[0], 'female': results[1]}
            return results
        else:
            return None
        
    @classmethod
    def get_population_data_by_block(cls, block_id, district_id):
        query = db.session.query(
            func.sum(cls.male_population).label('male'),
            func.sum(cls.female_population).label('female')
        ).filter(and_(cls.block_id==block_id, cls.district_id==district_id)
        ).group_by(cls.block_id)
        # query = cls.query.with_entities(cls.male_population, cls.female_population).filter_by(block_id=block_id)
        results = query.first() 
        if results:
            results = {
                'male': results[0], 
                'female': results[1]
                }
            return results
        else:
            return None

    @classmethod
    def get_runoff_area(cls, village_id):
        query = db.session.query(
                (CensusData.forest_area + CensusData.non_agriculture_area + CensusData.uncultivable_area).label('good_area'),
                (CensusData.grazing_area + CensusData.misc_area + CensusData.wasteland_area).label('average_area'),
                (CensusData.fallow_area + CensusData.current_fallow_area + CensusData.unirrigated_area +
                CensusData.canal_area + CensusData.tubewell_area + CensusData.tank_area + 
                CensusData.waterfall_area + CensusData.other_area).label('bad_area')
            ).filter(CensusData.village_id == village_id)
        results = query.first()

        if results:
            return {'good':round(float(results[0]),2), 
                    'average':round(float(results[1]), 2), 
                    'bad':round(float(results[2]),2)}
        else:
            return None
        
    @classmethod
    def get_runoff_by_block_id(cls, block_id):
        query = db.session.query(
            CensusData.block_id,
            func.sum((CensusData.forest_area + CensusData.non_agriculture_area + CensusData.uncultivable_area)).label('good_area'),
            func.sum((CensusData.grazing_area + CensusData.misc_area + CensusData.wasteland_area)).label('average_area'),
            func.sum((CensusData.fallow_area + CensusData.current_fallow_area + CensusData.unirrigated_area +
            CensusData.canal_area + CensusData.tubewell_area + CensusData.tank_area + 
            CensusData.waterfall_area + CensusData.other_area)).label('bad_area') 
        ).filter(CensusData.block_id == block_id
        ).group_by(CensusData.block_id)

        results = query.first()
        
        if results:
            return {'good':round(float(results[0]),2), 
                    'average':round(float(results[1]), 2), 
                    'bad':round(float(results[2]),2)}
        else:
            return None