from iWater.app.db import db

class Major_head(db.Model):
    __tablename__ = 'majour_head'

    id = db.Column(db.Integer, primary_key= True)
    major_head=db.Column(db.String(80),nullable=False)
    category_id = db.Column(db.Integer,nullable = False)

    
    def __init__(self,major_head,categoory_id):
        self.major_head=major_head
        self.category_id = categoory_id


    
    def json(self):
        return {
            'id': self.id,
            'major_head' : self.major_head,
            'category_id': self.category_id
            
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
        participant = Major_head.query.filter_by(id=_id).first()
        db.session.delete(participant)
        db.session.commit()

    def commit_db():
        db.session.commit()

    def update_db(data,_id):
        user = Major_head.query.filter_by(id=_id).update(data)
        db.session.commit()