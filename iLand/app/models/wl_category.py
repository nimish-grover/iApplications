from iLand.app.db import db

class WL_Category(db.Model):
    __tablename__ = 'wl_category'

    id = db.Column(db.Integer, primary_key= True)
    wl_category = db.Column(db.String(80),nullable=False)

    
    def __init__(self,wl_category):
        self.wl_category=wl_category

    
    def json(self):
        return {
            'id': self.id,
            'wl_category': self.wl_category
        }
    
    @classmethod
    def get_wl_category_by_id(cls, _id):
        query=cls.query.filter_by(id=_id).first()
        if query:
            return query.json()
        else:
            return None
    
    @classmethod
    def get_wl_category_by_name(cls, _name):
        query =  cls.query.filter_by(wl_category=_name).first()
        if query:
            return query.json()
        else:
            return None
    
    @classmethod
    def get_all(cls):
        query=cls.query.order_by(cls.wl_category)
        return query

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(_id):
        participant = WL_Category.query.filter_by(id=_id).first()
        db.session.delete(participant)
        db.session.commit()

    def commit_db():
        db.session.commit()

    def update_db(data,_id):
        user = WL_Category.query.filter_by(id=_id).update(data)
        db.session.commit()