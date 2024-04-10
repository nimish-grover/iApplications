from iLand.app.db import db
from sqlalchemy import func
from iLand.app.models.districts import District
from iLand.app.models.state import State

class Tga(db.Model):
    __tablename__ = 'tga'

    id = db.Column(db.Integer, primary_key= True)
    tga = db.Column(db.Float,nullable=False)
    district_id = db.Column(db.Integer,nullable=False)
    year_id = db.Column(db.Integer,nullable=False)
    
    def __init__(self,tga,district_id,year_id):
        self.tga=tga
        self.year_id = year_id
        self.district_id = district_id

    
    def json(self):
        return {
            'id': self.id,
            'tga': self.tga,
            'district_id': self.district_id,
            'year_id':self.year_id
        }
    
    @classmethod
    def get_tga_by_id(cls, _id):
        query=cls.query.filter_by(id=_id).first()
        if query:
            return query.json()
        else:
            return None
    
    @classmethod
    def get_tga_by_name(cls, _name):
        query =  cls.query.filter_by(tga=_name).first()
        if query:
            return query.json()
        else:
            return None
        
    @classmethod
    def get_tga_by_district_id(cls, _id):
        query =  cls.query.filter_by(district_id=_id).first()
        if query:
            return query.json()
        else:
            return None
    
    @classmethod
    def get_all(cls):
        query=cls.query.order_by(cls.tga)
        return query

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(_id):
        participant = Tga.query.filter_by(id=_id).first()
        db.session.delete(participant)
        db.session.commit()

    def commit_db():
        db.session.commit()

    def update_db(data,_id):
        user = Tga.query.filter_by(id=_id).update(data)
        db.session.commit()
        
    @classmethod
    def get_total_tga(cls):
        result = db.session.query(func.sum(cls.tga)).scalar()
        return result
    
    @classmethod
    def get_tga_state_wise(cls):
        result = db.session.query(State.name.label('state_name'), func.sum(cls.tga).label('total_tga')) \
                .join(District, District.code == cls.district_id) \
                .join(State, State.code == District.state_code) \
                .group_by(State.name) \
                .order_by(func.sum(cls.tga).desc()) \
                .all()
        return result
        
        """SELECT s.name AS state_name,
        SUM(t.tga) AS total_tga
        FROM tga t
        JOIN districts d ON t.district_id = d.code
        JOIN states s ON d.state_code = s.code
        GROUP BY s.name
        ORDER BY total_tga DESC;
        """
        
    @classmethod
    def get_tga_district_wise(cls,state_code):
        result = db.session.query(District.name.label('district_name'), func.sum(cls.tga).label('total_tga')) \
                .join(cls, cls.district_id == District.code) \
                .join(State, District.state_code == State.code) \
                .filter(State.code == state_code) \
                .group_by(District.name) \
                .order_by(func.sum(cls.tga).desc()) \
                .all()
        return result
        """SELECT d.name AS district_name,
        SUM(t.tga) AS total_tga
        FROM tga t
        JOIN districts d ON t.district_id = d.code
        JOIN states s ON d.state_code = s.code
        WHERE s.code = '6'
        GROUP BY d.name
        ORDER BY total_tga DESC"""