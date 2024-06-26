from iWater.app.db import db

class Crops(db.Model):
    __tablename__ = 'crops'

    id = db.Column(db.Integer, primary_key= True)
    name=db.Column(db.String(80),nullable=False)
    type_id = db.Column(db.Integer,nullable=False)
    water_required_per_hectare = db.Column(db.Float,nullable=False)

    
    def __init__(self,type_id,name,water_required_per_hectare):
        self.type_id=type_id
        self.name = name
        self.water_required_per_hectare = water_required_per_hectare

    
    def json(self):
        return {
            'id': self.id,
            'type_id': self.type_id,
            'name': self.name,
            'water_required_per_hectare' : self.water_required_per_hectare
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
    def check_existing(cls,crop_name):
        query = db.session.query(Crops).filter(Crops.name.ilike(f'%{crop_name.lower()}%')).first()
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
        participant = Crops.query.filter_by(id=_id).first()
        db.session.delete(participant)
        db.session.commit()

    def commit_db():
        db.session.commit()

    def update_db(data,_id):
        user = Crops.query.filter_by(id=_id).update(data)
        db.session.commit()