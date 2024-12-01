from iJalagam.app import db
from iJalagam.app.models import Block, District	

class GroundwaterExtraction(db.Model):
    __tablename__ = "groundwater_extractions"

    id = db.Column(db.Integer, primary_key=True)
    stage_of_extraction = db.Column(db.Float, nullable=False, default=0)
    rainfall = db.Column(db.Float, nullable=False, default=0)
    recharge = db.Column(db.Float, nullable=False, default=0)
    discharge = db.Column(db.Float, nullable=False, default=0)
    extractable = db.Column(db.Float, nullable=False, default=0)
    extraction = db.Column(db.Float, nullable=False, default=0)
    category = db.Column(db.String(80), nullable=False, default='')

    block_id = db.Column(db.ForeignKey('blocks.id'), nullable=False)
    district_id = db.Column(db.ForeignKey('districts.id'), nullable=False)

    block = db.relationship('Block')
    district = db.relationship('District')

    def __init__(self, stage_of_extraction, rainfall, recharge, 
                 discharge, extractable, extraction, category, 
                 block_id, district_id):
        self.stage_of_extraction = stage_of_extraction
        self.rainfall = rainfall
        self.recharge = recharge
        self.discharge = discharge
        self.extractable = extractable
        self.extraction = extraction
        self.category = category
        self.block_id = block_id
        self.district_id = district_id

    def json(self):
        return {
            'stage_of_extraction': self.stage_of_extraction,
            'rainfall': self.rainfall,
            'recharge': self.recharge,
            'discharge': self.discharge,
            'extractable': self.extractable,
            'extraction': self.extraction,
            'category': self.category,
            'block_id': self.block_id,
            'district_id': self.district_id
        }
    
    @classmethod
    def get_gw_by_block_id(cls, block_id, district_id):
        # SELECT id, stage_of_extraction, rainfall, recharge, discharge, extractable, extraction, category, block_id, district_id
        # FROM public.groundwater_extractions;
        query = db.session.query(
                cls.stage_of_extraction,
                cls.rainfall,
                cls.recharge, 
                cls.discharge,
                cls.extractable,
                cls.extraction,
                cls.category,
                Block.name.label('block_name'),
                District.name.label('district_name')
        ).join(Block, Block.id==cls.block_id
        ).join(District, District.id==cls.district_id
        ).filter(cls.block_id==block_id)

        result = query.first()
        if result:
            result = {
                'stage_of_extraction':round(result[0],2),
                'rainfall': round(result[1],2),
                'recharge': round(result[2],2),
                'discharge': round(result[3],2),
                'extractable': round(result[4],2),
                'extraction': round(result[5],2),
                'category': result[6],
                'block_name': result[7],
                'district_name':result[8]
            }
        else:
            result = {
                'stage_of_extraction':'NA',
                'rainfall': 0,
                'recharge': 0,
                'discharge': 0,
                'extractable': 0,
                'extraction': 0,
                'category': 'NA',
                'block_name': 'NA',
                'district_name':'NA'
            }
        
        return result