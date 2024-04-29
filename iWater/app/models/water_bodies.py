from app.db import db

class Water_bodies(db.Model):
    __tablename__ = 'water_bodies'

    id = db.Column(db.Integer, primary_key= True)
    district_code = db.Column(db.Integer)
    village_code = db.Column(db.Integer)
    wb_type_id = db.Column(db.Integer)
    water_spread_area = db.Column(db.Float)
    max_depth = db.Column(db.Float)
    storage_capacity = db.Column(db.Float)
    longitude = db.Column(db.String(80))
    lattitude = db.Column(db.String(80))

    
    def __init__(self,district_code,village_code,wb_type_id,water_spread_area,max_depth,storage_capacity,longitude,lattitude):
        self.district_code = district_code,
        self.village_code = village_code,
        self.wb_type_id = wb_type_id,
        self.water_spread_area = water_spread_area,
        self.max_depth = max_depth,
        self.storage_capacity = storage_capacity,
        self.longitude = longitude,
        self.lattitude = lattitude

    
    def json(self):
        return {
            'id': self.id,
            'district_code': self.district_code,
            'village_code' : self.village_code,
            'wb_type_id' : self.wb_type_id,
            'water_spread_area' : self.water_spread_area,
            'max_depth' : self.max_depth,
            'storage_capacity' : self.storage_capacity,
            'longitude' : self.longitude,
            'lattitude' : self.lattitude
        }
    
    @classmethod
    def get_wb_by_code(cls, _code):
        query=cls.query.filter_by(code=_code).first()
        if query:
            return query.json()
        else:
            return None
    
    @classmethod
    def get_wb_by_name(cls, _name):
        query =  cls.query.filter_by(name=_name).first()
        if query:
            return query.json()
        else:
            return None
    
    @classmethod
    def get_all(cls):
        query=cls.query.order_by(cls.name)
        return query

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(_code):
        participant = Water_bodies.query.filter_by(code=_code).first()
        db.session.delete(participant)
        db.session.commit()

    def commit_db():
        db.session.commit()

    def update_db(data,_code):
        user = Water_bodies.query.filter_by(code=_code).update(data)
        db.session.commit()