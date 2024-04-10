from iLand.app.db import db

class Years(db.Model):
    __tablename__ = 'years'

    id = db.Column(db.Integer, primary_key= True)
    year = db.Column(db.String(80),nullable=False)

    
    def __init__(self,year):
        self.year=year

    
    def json(self):
        return {
            'id': self.id,
            'year': self.year
        }
    
    @classmethod
    def get_year_by_id(cls, _id):
        query=cls.query.filter_by(id=_id).first()
        if query:
            return query.json()
        else:
            return None
    
    @classmethod
    def get_year_by_name(cls, _name):
        query =  cls.query.filter_by(year=_name).first()
        if query:
            return query.json()
        else:
            return None
    
    @classmethod
    def get_all(cls):
        query=cls.query.order_by(cls.year)
        return query

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(_id):
        participant = Years.query.filter_by(id=_id).first()
        db.session.delete(participant)
        db.session.commit()

    def commit_db():
        db.session.commit()

    def update_db(data,_id):
        user = Years.query.filter_by(id=_id).update(data)
        db.session.commit()