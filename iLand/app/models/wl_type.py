from iLand.app.db import db

class WL_Type(db.Model):
    __tablename__ = 'wl_type'

    id = db.Column(db.Integer, primary_key= True)
    wl_type = db.Column(db.String(80),nullable=False)
    wl_category_id = db.Column(db.Integer)
    
    def __init__(self,wl_type,wl_category_id):
        self.wl_type=wl_type
        self.wl_category_id = wl_category_id

    
    def json(self):
        return {
            'id': self.id,
            'wl_type': self.wl_type,
            'wl_category_id': self.wl_category_id
        }
    
    @classmethod
    def get_wl_type_by_id(cls, _id):
        query=cls.query.filter_by(id=_id).first()
        if query:
            return query.json()
        else:
            return None
    
    @classmethod
    def get_wl_type_by_name(cls, _name):
        query =  cls.query.filter_by(wl_type=_name).first()
        if query:
            return query.json()
        else:
            return None
        
    @classmethod
    def get_wl_type_by_category_id(cls, _id):
        query =  cls.query.filter_by(wl_category_id=_id).first()
        if query:
            return query.json()
        else:
            return None
    
    @classmethod
    def get_all(cls):
        query=cls.query.order_by(cls.wl_type)
        return query

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(_id):
        participant = WL_Type.query.filter_by(id=_id).first()
        db.session.delete(participant)
        db.session.commit()

    def commit_db():
        db.session.commit()

    def update_db(data,_id):
        user = WL_Type.query.filter_by(id=_id).update(data)
        db.session.commit()