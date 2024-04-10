from iLand.app.db import db
from iLand.app.models.districts import District
from iLand.app.models.state import State
from iLand.app.models.wl_category import WL_Category
from iLand.app.models.wl_type import WL_Type
from sqlalchemy import func

class WL_Area(db.Model):
    __tablename__ = 'wl_area'

    id = db.Column(db.Integer, primary_key= True)
    wl_area = db.Column(db.Float,nullable=False)
    wl_type_id = db.Column(db.Integer)
    district_id = db.Column(db.Integer)
    year_id = db.Column(db.Integer)
    
    def __init__(self,wl_area,wl_type_id,district_id,year_id):
        self.wl_area=wl_area
        self.wl_type_id = wl_type_id
        self.year_id = year_id
        self.district_id = district_id

    
    def json(self):
        return {
            'id': self.id,
            'wl_area': self.wl_area,
            'wl_type_id': self.wl_type_id,
            'district_id': self.district_id,
            'year_id':self.year_id
        }
    
    @classmethod
    def get_wl_area_by_id(cls, _id):
        query=cls.query.filter_by(id=_id).first()
        if query:
            return query.json()
        else:
            return None
    
    @classmethod
    def get_wl_area_by_name(cls, _name):
        query =  cls.query.filter_by(wl_area=_name).first()
        if query:
            return query.json()
        else:
            return None
        
    @classmethod
    def get_wl_area_by_category_id(cls, _id):
        query =  cls.query.filter_by(wl_category_id=_id).first()
        if query:
            return query.json()
        else:
            return None
    
    @classmethod
    def get_all(cls):
        query=cls.query.order_by(cls.wl_area)
        return query

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(_id):
        participant = WL_Area.query.filter_by(id=_id).first()
        db.session.delete(participant)
        db.session.commit()

    def commit_db():
        db.session.commit()

    def update_db(data,_id):
        user = WL_Area.query.filter_by(id=_id).update(data)
        db.session.commit()

    @classmethod
    def get_area_state_wise(cls):
        result = db.session.query(State.name.label('state_name'), func.sum(cls.wl_area).label('total_wl_area')) \
                .join(District, District.state_code == State.code) \
                .join(cls, cls.district_id == District.code) \
                .group_by(State.name) \
                .order_by(func.sum(cls.wl_area)) \
                .all()
        return result
        """SELECT s.name AS state_name,
        SUM(w.wl_area) AS total_wl_area
        FROM wl_area w
        JOIN districts d ON w.district_id = d.code
        JOIN states s ON d.state_code = s.code
        GROUP BY s.name 
        ORDER BY total_wl_area DESC;"""
        
        
    @classmethod
    def get_area_district_wise(cls,state_code):
        result = db.session.query(District.name.label('district_name'), func.sum(cls.wl_area).label('total_wl_area')) \
                    .join(cls, cls.district_id == District.code) \
                    .join(State, District.state_code == State.code) \
                    .filter(State.code == state_code) \
                    .group_by(District.name) \
                    .order_by(func.sum(cls.wl_area).desc()) \
                    .all()
        return result
        """SELECT d.name AS district_name,
        SUM(w.wl_area) AS total_wl_area
        FROM wl_area w
        JOIN districts d ON w.district_id = d.code
        JOIN states s ON d.state_code = s.code
        WHERE s.code = 6
        GROUP BY d.name
        ORDER BY total_wl_area DESC;"""
        
        
    @classmethod
    def get_area_category_wise(cls):
        result = db.session.query(WL_Category.wl_category.label('category'), func.sum(cls.wl_area).label('total_wl_area')) \
                .join(WL_Type, cls.wl_type_id == WL_Type.id) \
                .join(WL_Category, WL_Type.wl_category_id == WL_Category.id) \
                .group_by(WL_Category.wl_category) \
                .all()
        
        """SELECT c.wl_category AS category,
        SUM(w.wl_area) AS total_wl_area
        FROM wl_area w
        JOIN wl_type t ON w.wl_type_id = t.id
        JOIN wl_category c ON t.wl_category_id = c.id
        GROUP BY c.wl_category;"""
        
    @classmethod
    def get_total_area(cls):
        result = db.session.query(func.sum(cls.wl_area)).scalar()
        return result
    
    
    @classmethod
    def get_district_area_category_wise(cls,district_code):
        result = db.session.query(WL_Category.wl_category.label('category'), func.sum(cls.wl_area).label('total_wl_area')) \
                .join(WL_Type, cls.wl_type_id == WL_Type.id) \
                .join(WL_Category, WL_Type.wl_category_id == WL_Category.id) \
                .join(District, cls.district_id == District.code) \
                .filter(District.code == district_code) \
                .group_by(WL_Category.wl_category) \
                .all()
                
        return result
        """SELECT c.wl_category AS category,
        SUM(w.wl_area) AS total_wl_area
        FROM wl_area w
        JOIN wl_type t ON w.wl_type_id = t.id
        JOIN wl_category c ON t.wl_category_id = c.id
        JOIN districts d ON w.district_id = d.code
        WHERE d.code = 188
        GROUP BY c.wl_category;
        """