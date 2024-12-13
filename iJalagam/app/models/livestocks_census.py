from sqlalchemy import func
from iJalagam.app.db import db
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
    def get_livestock_by_block(cls, block_id, district_id):
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
                        'coefficient':row.coefficient } 
                        for row in results]
            return json_data
        return None
