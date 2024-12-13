from sqlalchemy import func
from iJalagam.app.db import db
from iJalagam.app.models.blocks import Block
from iJalagam.app.models.districts import District
from iJalagam.app.models.lulc import LULC
from iJalagam.app.models.territory import TerritoryJoin

class LULCCensus(db.Model):
    __tablename__ = 'lulc_census'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    lulc_id = db.Column(db.Integer, db.ForeignKey('lulc.id'), nullable=False)
    lulc_area = db.Column(db.Float, nullable=False)
    tj_id = db.Column(db.Integer, db.ForeignKey('territory_joins.id'), nullable=False)

    # Relationships
    lulc = db.relationship('LULC', backref=db.backref('lulc_census', lazy="dynamic"))
    territory_join = db.relationship('TerritoryJoin', backref=db.backref('lulc_census', lazy="dynamic"))

    def __init__(self, lulc_id, lulc_area, tj_id):
        self.lulc_id = lulc_id
        self.lulc_area = lulc_area
        self.tj_id = tj_id

    def __repr__(self):
        return f"<LULCCensus(id={self.id}, lulc_id={self.lulc_id}, lulc_area={self.lulc_area}, tj_id={self.tj_id})>"

    def json(self):
        return {
            "id": self.id,
            "lulc_id": self.lulc_id,
            "lulc_area": self.lulc_area,
            "tj_id": self.tj_id
        }
    
    @classmethod
    def get_lulc_by_block(cls, block_id, district_id):
        query = db.session.query(
                func.sum(cls.lulc_area).label('catchment_area'),
                LULC.catchment,
            ).join(TerritoryJoin, TerritoryJoin.id==cls.tj_id
            ).join(LULC, LULC.id==cls.lulc_id
            ).join(Block, Block.id == TerritoryJoin.block_id
            ).join(District, District.id==TerritoryJoin.district_id
            ).filter(
                Block.id == block_id, 
                District.id == district_id
            ).group_by(LULC.catchment)
        
        results = query.all()

        if results:
            json_data = [{
                'catchment': row.catchment,
                'catchment_area': row.catchment_area
            } for row in results]
            return json_data
        return None
    
    
    @classmethod
    def get_area_by_block(cls,block_id,district_id):
        query = (
            db.session.query(
                func.sum(LULCCensus.lulc_area).label('lulc_area'),  # SUM(lulc_area)
                LULCCensus.lulc_id.label('lulc_id')  # lulc_id
            )
            .join(TerritoryJoin, TerritoryJoin.id == LULCCensus.tj_id)  # JOIN territory_joins
            .join(Block, Block.id == TerritoryJoin.block_id)  # JOIN blocks
            .join(District, District.id == TerritoryJoin.district_id)  # JOIN districts
            .filter(
                Block.id == block_id,  # WHERE blocks.id = 2074
                District.id == district_id  # WHERE districts.id = 745
            )
            .group_by(LULCCensus.lulc_id) )
        
        results = query.all()
        if results:
            json_data = [{
            'lulc area':row.lulc_area,
            'lulc_id':row.lulc_id
            } for row in results]
            return json_data
        return None
        