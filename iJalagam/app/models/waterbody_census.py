from sqlalchemy import func
from iJalagam.app import db
from iJalagam.app.models.waterbody_type import WaterbodyType


class WaterbodyCensus(db.Model):
    __tablename__ = "waterbodies_census"

    id = db.Column(db.Integer, primary_key=True)
    spread_area = db.Column(db.Float, nullable=False, default=0)
    storage_capacity = db.Column(db.Float, nullable=False, default=0)
    max_depth = db.Column(db.Float, nullable=False, default=0)
    longitude = db.Column(db.String(80))
    latitude = db.Column(db.String(80))

    waterbody_type_id = db.Column(db.ForeignKey('waterbody_types.id'), nullable=False)
    village_id = db.Column(db.ForeignKey('villages.id'), nullable=False)
    block_id = db.Column(db.ForeignKey('blocks.id'), nullable=False)
    district_id = db.Column(db.ForeignKey('districts.id'), nullable=False)  

    waterbody = db.relationship('WaterbodyType')
    village = db.relationship('Village')
    block = db.relationship('Block')
    district = db.relationship('District')

    def __init__(self, spread_area, storage_capacity, max_depth, longitude, latitude, waterbody_type_id, village_id, block_id, district_id):
        self.spread_area = spread_area
        self.storage_capacity = storage_capacity
        self.max_depth = max_depth
        self.longitude = longitude
        self.latitude = latitude
        self.waterbody_type_id = waterbody_type_id
        self.village_id = village_id
        self.block_id = block_id
        self.district_id = district_id

    def json(self):
        return {
            'spread_area': self.spread_area,
            'storage_capacity': self.storage_capacity,
            'max_depth': self.max_depth,
            'longitude': self.longitude,
            'latitude': self.latitude,
            'waterbody_type_id': self.waterbody_type_id,
            'village_id': self.village_id,
            'block_id': self.block_id,
            'district_id': self.district_id
        }

    @classmethod
    def get_waterbody_by_panchayat_id(cls, village_id):
        print('hello classmethod')
        return cls.json(cls.query.filter_by(village_id = village_id).first())
    
    @classmethod
    def get_waterbodies_by_village_id(cls, village_id):
        query = db.session.query(
            cls.id,
            cls.district_id,
            cls.block_id,
            cls.village_id,
            cls.spread_area,
            cls.storage_capacity,
            cls.max_depth,
            cls.longitude,
            cls.latitude,
            WaterbodyType.id.label('waterbody_type_id'),
            WaterbodyType.waterbody_type
        ).join(WaterbodyType, WaterbodyType.id == cls.waterbody_type_id
        ).filter(cls.village_id == village_id)

        results = query.all()

        if results:
            result = [{
                'id':item.id,
                'spread_area': item.spread_area,
                'storage_capacity': item.storage_capacity,
                'max_depth': item.max_depth,
                'longitude': item.longitude,
                'latitude': item.latitude,
                'waterbody_type': item.waterbody_type
            } for item in results]
            return result
        else:
            return None
    
    # select wt.waterbody_type, count(waterbody_type_id), sum(spread_area), 
    # sum(storage_capacity), avg(max_depth) 
    # from waterbodies_census wc 
    # inner join waterbody_types wt on wt.id = wc.waterbody_type_id
    # where village_id = 930 
    # group by wt.waterbody_type

    @classmethod
    def get_count_by_id(cls, _id):
        query = db.session.query(
            WaterbodyType.id.label('waterbody_type_id'),
            WaterbodyType.waterbody_type.label('waterbody_type'),
            func.coalesce(func.count(cls.village_id).label('count'),0),
            func.coalesce(func.sum(cls.spread_area).label('spread_area'),0),
            func.coalesce(func.sum(cls.storage_capacity).label('storage_capacity'),0),
            func.coalesce(func.avg(cls.max_depth).label('max_depth'),0)
        ).outerjoin(
            cls, (WaterbodyType.id == cls.waterbody_type_id) & (cls.village_id==_id)
        ).group_by(WaterbodyType.waterbody_type, WaterbodyType.id)

        results = query.all()

        if results: 
            json_data =  [{
                'waterbody_type_id': result[0],
                'waterbody_type': result[1],
                'count': result[2],
                'spread_area': round(result[3],2),
                'storage_capacity': round(result[4],2),
                'depth': round(result[5],2)            
            } for result in results]
            return json_data
        else:
            return None

    @classmethod   
    def get_count_by_block_id(cls, block_id, district_id):
        query=db.session.query(
            WaterbodyType.id.label('waterbody_type_id'),
            WaterbodyType.waterbody_type.label('waterbody_type'),
            func.coalesce(func.count(cls.village_id).label('count'),0),
            func.coalesce(func.sum(cls.spread_area).label('spread_area'),0),
            func.coalesce(func.sum(cls.storage_capacity).label('storage_capacity'),0),
            func.coalesce(func.avg(cls.max_depth).label('max_depth'),0)
        ).outerjoin(
            cls, (WaterbodyType.id == cls.waterbody_type_id) & (cls.block_id==block_id)
        ).group_by(WaterbodyType.waterbody_type, WaterbodyType.id)

        results = query.all()

        if results: 
            json_data =  [{
                'waterbody_type_id': result[0],
                'waterbody_type': result[1],
                'count': result[2],
                'spread_area': round(result[3],2),
                'storage_capacity': round(result[4],2),
                'depth': round(result[5],2)            
            } for result in results]
            return json_data
        else:
            return None