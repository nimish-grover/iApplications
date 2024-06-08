from iWater.app.db import db

class Crop_area(db.Model):
    __tablename__ = 'crop_area'

    id = db.Column(db.Integer, primary_key= True)
    district_code=db.Column(db.Integer,nullable=False)
    village_code=db.Column(db.Integer,nullable=False)
    crop_id=db.Column(db.Integer,nullable=False)
    crop_type_id=db.Column(db.Integer,nullable=False)
    crop_area = db.Column(db.Float,nullable=False)

    
    def __init__(self,type_id,district_code,village_code,crop_id,crop_type_id,crop_area):
        self.type_id=type_id
        self.crop_area = crop_area
        self.district_code = district_code
        self.village_code = village_code
        self.crop_id = crop_id
        self.crop_type_id = crop_type_id

    
    def json(self):
        return {
            'id': self.id,
            'crop_type_id': self.crop_type_id,
            'crop_area': self.crop_area,
            'district_code' : self.district_code,
            'village_code' : self.village_code,
            'crop_id' : self.crop_id,
            'crop_type_id' : self.crop_type_id
        }
    
    @classmethod
    def get_wb_by_id(cls, _id):
        query=cls.query.filter_by(id=_id).first()
        if query:
            return query.json()
        else:
            return None
    
    @classmethod
    def get_wb_by_type_id(cls, _type_id):
        query =  cls.query.filter_by(type_id=_type_id).first()
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

    def delete_from_db(_id):
        participant = Crop_area.query.filter_by(id=_id).first()
        db.session.delete(participant)
        db.session.commit()

    def commit_db():
        db.session.commit()

    def update_db(data,_id):
        user = Crop_area.query.filter_by(id=_id).update(data)
        db.session.commit()