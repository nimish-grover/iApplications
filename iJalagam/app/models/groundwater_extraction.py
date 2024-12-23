from sqlalchemy import func
from iJalagam.app.db import db
from iJalagam.app.models import Block, District
from iJalagam.app.models.block_ground import BlockGround
from iJalagam.app.models.block_territory import BlockTerritory	

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
    tj_id = db.Column(db.ForeignKey('territory_joins.id'), nullable=False)

    block = db.relationship('Block', backref=db.backref("groundwater_extractions", lazy="dynamic"))
    district = db.relationship('District', backref=db.backref("groundwater_extractions", lazy="dynamic"))
    territory_join = db.relationship("TerritoryJoin", backref=db.backref("groundwater_extractions", lazy="dynamic"))

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
    def get_census_data_groundwater(cls, block_id, district_id):
        query = db.session.query(
                cls.extractable,
                cls.extraction,
                cls.stage_of_extraction,
                cls.category,
                cls.block_id.label('block_id')
        ).join(Block, Block.id==cls.block_id
        ).join(District, District.id==cls.district_id
        ).filter(cls.block_id==block_id, District.id==district_id)

        results = query.all()

        if results:
            json_data = [{
                'extractable': round(row.extractable, 2),
                'extraction': round(row.extraction, 2),
                'stage_of_extraction': round(row.stage_of_extraction,2),
                'category': row.category
            } for row in results]
            return json_data
        return None
        
    @classmethod
    def get_groudwater_by_block(cls, block_id, district_id):
        block_groundwater_subquery = db.session.query(
                BlockGround.extraction.label("extraction"),
                Block.lgd_code.label("lgd_code")            
            ).join(BlockTerritory, BlockTerritory.id == BlockGround.bt_id
            ).join(Block, Block.id == BlockTerritory.block_id
            ).filter(Block.id == block_id
            ).subquery()

        # Main query
        query = db.session.query(
                GroundwaterExtraction.extractable,
                func.coalesce(block_groundwater_subquery.c.extraction, GroundwaterExtraction.extraction).label("extraction"),
                GroundwaterExtraction.stage_of_extraction,
                GroundwaterExtraction.category,
                GroundwaterExtraction.block_id.label("block_id"),            
            ).join(Block, Block.id == GroundwaterExtraction.block_id
            ).join(BlockTerritory, BlockTerritory.block_id == GroundwaterExtraction.block_id
            ).outerjoin(block_groundwater_subquery, block_groundwater_subquery.c.lgd_code == Block.lgd_code
            ).filter(Block.id == block_id)
        
        results = query.all()

        if results:
            json_data = [{
                'extractable': round(row.extractable, 2),
                'extraction': round(row.extraction, 2),
                'stage_of_extraction': round(row.stage_of_extraction,2),
                'category': row.category
            } for row in results]
            return json_data
        return None