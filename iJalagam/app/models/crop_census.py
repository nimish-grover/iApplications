from sqlalchemy import func
from iJalagam.app.db import db
from iJalagam.app.models.block_crops import BlockCrop
from iJalagam.app.models.block_territory import BlockTerritory
from iJalagam.app.models.blocks import Block
from iJalagam.app.models.crops import Crop
from iJalagam.app.models.territory import TerritoryJoin

class CropCensus(db.Model):
    __tablename__ = 'crop_census'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    territory_id = db.Column(db.Integer, db.ForeignKey('territory_joins.id'), nullable=False)
    village_lgd_code = db.Column(db.Integer, db.ForeignKey('villages.lgd_code'), nullable=False)
    crop_id = db.Column(db.Integer, db.ForeignKey('crops.id'), nullable=False)
    season = db.Column(db.String(50), nullable=False)
    crop_area = db.Column(db.Float, nullable=False)
    production = db.Column(db.Float, nullable=False)
    crop_yield = db.Column(db.Float, nullable=False)

    # Relationships
    territory = db.relationship('TerritoryJoin', backref=db.backref('crop_census', lazy="dynamic"))
    village = db.relationship('Village', backref=db.backref('crop_census', lazy="dynamic"))
    crop = db.relationship('Crop', backref=db.backref('crop_census', lazy="dynamic"))

    def __init__(self, territory_id, village_lgd_code, crop_id, season, crop_area, production, crop_yield):
        """
        Initialize the CropCensus instance with the provided attributes.
        """
        self.territory_id = territory_id
        self.village_lgd_code = village_lgd_code
        self.crop_id = crop_id
        self.season = season
        self.crop_area = crop_area
        self.production = production
        self.crop_yield = crop_yield

    def __repr__(self):
        """
        Provides a string representation of the CropCensus instance.
        """
        return (f"<CropCensus(id={self.id}, territory_id={self.territory_id}, "
                f"village_lgd_code={self.village_lgd_code}, crop_id={self.crop_id}, "
                f"season='{self.season}', crop_area={self.crop_area}, production={self.production}, "
                f"crop_yield={self.crop_yield})>")

    def json(self):
        """
        Returns a JSON serializable dictionary representation of the CropCensus instance.
        """
        return {
            "id": self.id,
            "territory_id": self.territory_id,
            "village_lgd_code": self.village_lgd_code,
            "crop_id": self.crop_id,
            "season": self.season,
            "crop_area": self.crop_area,
            "production": self.production,
            "crop_yield": self.crop_yield
        }
    
    @classmethod
    def get_census_data_crops(cls, block_id, district_id):
        query = db.session.query(
            func.sum(cls.crop_area).label('crop_area'),
            Crop.id.label('crop_id'),
            Crop.coefficient,
            Crop.crop_name
        ).join(Crop, Crop.id == cls.crop_id
        ).join(TerritoryJoin, TerritoryJoin.id == cls.territory_id
        ).filter(
            TerritoryJoin.block_id==block_id,
            TerritoryJoin.district_id==district_id
        ).group_by(
            Crop.id,Crop.coefficient,Crop.crop_name
        )
        results = query.all()
        if results:
            json_data = [{
                        'entity_id':row.crop_id,
                        'entity_value':row.crop_area, 
                        'entity_name':row.crop_name,
                        'coefficient':row.coefficient }
                          for row in results]
            return json_data
        return None
    
    @classmethod
    def get_crops_by_block(cls, block_id, district_id):
        block_crops_subquery = (
            db.session.query(
                BlockCrop.crop_id.label("crop_id"),
                func.sum(BlockCrop.area).label("total_area")
            )
            .join(BlockTerritory, BlockTerritory.id == BlockCrop.bt_id)
            .join(Block, Block.id == BlockTerritory.block_id)
            .filter(Block.id == block_id)
            .group_by(BlockCrop.crop_id)
            .subquery()
        )

        # Subquery for crop_census
        crop_census_subquery = db.session.query(
                CropCensus.crop_id.label("crop_id"),
                func.sum(CropCensus.crop_area).label("total_area")
                ).join(TerritoryJoin, TerritoryJoin.id == CropCensus.territory_id
                ).join(Block, Block.id == TerritoryJoin.block_id\
                ).filter(Block.id == block_id
                ).group_by(CropCensus.crop_id
                ).subquery()

        # Main query
        query = db.session.query(
                Crop.crop_name,
                Crop.id.label("crop_id"),
                Crop.coefficient,
                func.coalesce(block_crops_subquery.c.total_area, crop_census_subquery.c.total_area, 0).label("crop_area"),
                ).outerjoin(block_crops_subquery, block_crops_subquery.c.crop_id == Crop.id
                ).outerjoin(crop_census_subquery, crop_census_subquery.c.crop_id == Crop.id)
            
        results = query.all()
        if results:
            json_data = [{
                        'entity_id':row.crop_id,
                        'entity_value':row.crop_area, 
                        'entity_name':row.crop_name,
                        'coefficient':row.coefficient }
                          for row in results]
            return json_data
        return None