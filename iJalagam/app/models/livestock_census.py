from sqlalchemy import and_, func
from iJalagam.app import db
from iJalagam.app.models.blocks import Block 
from iJalagam.app.models.coefficients import Coefficient
from iJalagam.app.models.districts import District
from iJalagam.app.models.livestock import Livestock


class LivestockCensus(db.Model):
    __tablename__ = 'livestock_census'

    id = db.Column(db.Integer, primary_key = True)
    coefficient_id = db.Column(db.ForeignKey('coefficients.id'), nullable=False)
    livestock_quantity = db.Column(db.Integer, nullable=False, default=0)
    village_id = db.Column(db.ForeignKey('villages.id'), nullable=False)
    block_id = db.Column(db.ForeignKey('blocks.id'), nullable=False)
    district_id = db.Column(db.ForeignKey('districts.id'), nullable=False)
    livestock_id = db.Column(db.ForeignKey('livestocks.id'))

    coefficient = db.relationship('Coefficient')
    village = db.relationship('Village')
    block = db.relationship('Block')
    district = db.relationship('District')

    def __init__(self, coefficient_id, livestock_quantity, village_id, block_id, district_id ):
        self.coefficient_id = coefficient_id
        self.livestock_quantity = livestock_quantity
        self.village_id = village_id
        self.block_id = block_id
        self.district_id = district_id

    def json(self):
        return {
            'coefficient_id': self.coefficient_id,
            'livestock_quantity': self.livestock_quantity,
            'village_id': self.village_id,
            'block_id': self.block_id,
            'district_id': self.district_id
        }
    
    @classmethod
    def get_livestock_by_village_id(cls, _id):        
        query = db.session.query(
            cls.livestock_quantity, 
            Coefficient.name,
            Coefficient.coefficient,
        ).join(
            Coefficient, Coefficient.id == cls.coefficient_id
        ).filter(
            cls.village_id ==_id
        )

        results = query.all()

        if results:
            json_data = [{
                'count':result[0], 
                'livestock':result[1], 
                'consumption': float(result[2]) * 365 * int(result[0])
                    } for result in results]
            print(json_data)
            return json_data
        else:
            return None
        
    
    @classmethod
    def get_livestock_by_block_id(cls, block_id, district_id):
        query = db.session.query(
            Livestock.id,
            func.coalesce(func.sum(cls.livestock_quantity.label('count')),0),
            Livestock.name.label('livestock'),
            func.avg(Livestock.coefficient).label('coefficient')
        ).outerjoin(
            cls, (Livestock.id == cls.livestock_id) & (cls.block_id==block_id)
        ).group_by(Livestock.name, Livestock.id
        ).order_by(Livestock.id)

        # ).join(Livestock, Livestock.id == cls.livestock_id
        # ).filter(and_(cls.block_id==block_id, cls.district_id==district_id)
        # ).group_by(Livestock.name)
        
        results = query.all()

        if results:
            json_data = [{'count': result[1],'livestock':result[2], 'coefficient': result[3]} for result in results]
            return json_data
        else:
            return None
