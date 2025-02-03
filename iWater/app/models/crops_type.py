from iWater.app.db import db

class Crops_type(db.Model):
    __tablename__ = 'crops_type'

    id = db.Column(db.Integer, primary_key= True)
    type = db.Column(db.String,nullable=False)

    
    def __init__(self,type):
        self.type=type

    
    def json(self):
        return {
            'id': self.id,
            'type': self.type
        }
    
    @classmethod
    def get_wb_by_id(cls, _id):
        query=cls.query.filter_by(id=_id).first()
        if query:
            return query.json()
        else:
            return None
    
    @classmethod
    def get_by_type(cls, _type):
        query =  cls.query.filter_by(type=_type).first()
        if query:
            return query.json()
        else:
            return None
    
    @classmethod
    def get_all(cls):
        query=cls.query.order_by(cls.id).all()
        arr =[]
        for row in query:
            row.json()
            arr.append(row)
        return arr

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(_id):
        participant = Crops_type.query.filter_by(id=_id).first()
        db.session.delete(participant)
        db.session.commit()

    def commit_db():
        db.session.commit()

    def update_db(data,_id):
        user = Crops_type.query.filter_by(id=_id).update(data)
        db.session.commit()