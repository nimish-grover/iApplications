from sqlalchemy import func
from iJalagam.app.db import db
from iJalagam.app.models.block_livestocks import BlockLivestock
from iJalagam.app.models.block_territory import BlockTerritory
from iJalagam.app.models.blocks import Block
from iJalagam.app.models.livestocks import Livestock
from iJalagam.app.models.territory import TerritoryJoin

class LivestockCensus(db.Model):
    __tablename__ = 'livestock_census'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    livestock_id = db.Column(db.Integer, db.ForeignKey('livestocks.id'), nullable=True)
    livestock_count = db.Column(db.Integer, nullable=False)
    village_code = db.Column(db.Integer, nullable=False)
    block_code = db.Column(db.Integer, nullable=False)
    district_code = db.Column(db.Integer, nullable=False)
    tj_id = db.Column(db.Integer, db.ForeignKey('territory_joins.id'), nullable=True)

    # Relationships
    livestock = db.relationship("Livestock", backref=db.backref("livestock_census", lazy="dynamic"))
    territory_join = db.relationship("TerritoryJoin", backref=db.backref("livestock_census", lazy="dynamic"))

    def __init__(self, livestock_count, village_code, block_code, district_code, livestock_id=None, tj_id=None):
        self.livestock_count = livestock_count
        self.village_code = village_code
        self.block_code = block_code
        self.district_code = district_code
        self.livestock_id = livestock_id
        self.tj_id = tj_id

    def __repr__(self):
        return (f"<LivestockCensus(id={self.id}, livestock_count={self.livestock_count}, "
                f"village_code={self.village_code}, block_code={self.block_code}, "
                f"district_code={self.district_code}, livestock_id={self.livestock_id}, "
                f"tj_id={self.tj_id})>")

    def json(self):
        return {
            "id": self.id,
            "livestock_count": self.livestock_count,
            "village_code": self.village_code,
            "block_code": self.block_code,
            "district_code": self.district_code,
            "livestock_id": self.livestock_id,
            "tj_id": self.tj_id
        }
    
    @classmethod
    def get_census_data_livestock(cls, block_id, district_id):
        query = db.session.query(
            func.sum(cls.livestock_count).label('livestock_count'),
            Livestock.livestock_name,
            Livestock.id.label('livestock_id'),
            Livestock.coefficient.label('coefficient')
        ).join(Livestock, Livestock.id==cls.livestock_id
        ).join(TerritoryJoin, TerritoryJoin.id == cls.tj_id
        ).filter(
            TerritoryJoin.block_id == block_id,
            TerritoryJoin.district_id == district_id
        ).group_by(
            TerritoryJoin.block_id,
            TerritoryJoin.district_id,
            Livestock.id,
            Livestock.livestock_name,
            Livestock.coefficient
        ).order_by(
            Livestock.livestock_name
        )
        results = query.all()
        if results:
            json_data = [{
                        'entity_id':row.livestock_id,
                        'entity_value':row.livestock_count, 
                        'entity_name':row.livestock_name,
                        'coefficient':row.coefficient 
                        } 
                        for row in results]
            return json_data
        return None
    
    @classmethod
    def get_livestock_by_block(cls, block_id, district_id):
        block_livestocks_subquery = db.session.query(
                BlockLivestock.livestock_id.label("livestock_id"),
                func.sum(BlockLivestock.count).label("total_count")
            ).join(BlockTerritory, BlockTerritory.id == BlockLivestock.bt_id
            ).join(Block, Block.id == BlockTerritory.block_id
            ).filter(Block.id == block_id
            ).group_by(BlockLivestock.livestock_id
            ).subquery()

        # Subquery for livestock_census
        livestock_census_subquery = db.session.query(
                LivestockCensus.livestock_id.label("livestock_id"),
                func.sum(LivestockCensus.livestock_count).label("total_count")
            ).join(TerritoryJoin, TerritoryJoin.id == LivestockCensus.tj_id
            ).join(Block, Block.id == TerritoryJoin.block_id
            ).filter(Block.id == block_id
            ).group_by(LivestockCensus.livestock_id
            ).subquery()

        # Main query
        query = db.session.query(
                Livestock.livestock_name,
                Livestock.id.label("livestock_id"),
                Livestock.coefficient.label("coefficient"),
                func.coalesce(block_livestocks_subquery.c.total_count, livestock_census_subquery.c.total_count, 0).label("livestock_count")
            ).outerjoin(block_livestocks_subquery, block_livestocks_subquery.c.livestock_id == Livestock.id
            ).outerjoin(livestock_census_subquery, livestock_census_subquery.c.livestock_id == Livestock.id
            ).order_by(Livestock.id)
        
        results = query.all()
        if results:
            json_data = [{
                        'entity_id':row.livestock_id,
                        'entity_value':row.livestock_count, 
                        'entity_name':row.livestock_name,
                        'coefficient':row.coefficient } 
                        for row in results]
            return json_data
        return None
